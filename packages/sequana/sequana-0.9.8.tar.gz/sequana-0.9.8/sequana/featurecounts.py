# -*- coding: utf-8 -*-
#
#  This file is part of Sequana software
#
#  Copyright (c) 2016,2020 - Sequana Development Team
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#      Etienne Kornobis <etienne.kornobis@pasteur.fr>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import re
from pathlib import Path

import pandas as pd

from sequana.lazy import pylab
from sequana import logger

logger.name = __name__


__all__ = ['get_most_probable_strand_consensus', 'get_most_probable_strand',
    'MultiFeatureCount', 'FeatureCount']


def get_most_probable_strand(sample_folder, tolerance):
    """Return total counts by strand from featureCount matrix folder, strandness and
    probable strand for a single sample (using a tolerance threshold for
    strandness). This assumes a single sample by featureCounts file.

    Possible values include: 0 (unstranded), 1 (stranded) and 2 (reversely stranded).

    We compute the number of counts in case 1 and 2 and compute the variable the
    RS = stranded / (stranded + reversely stranded ).

    If RS < tolerance, reversely stranded
    If RS in 0.5+-tolerance: unstranded.
    If RS > 1-tolerance, stranded
    Otherwise, we cannot decided.

    """
    sample_folder = Path(sample_folder)
    fc_files = sample_folder.glob("feature_counts_*/*_feature.out")

    sample_name = sample_folder.stem
    res_dict = {}

    for f in fc_files:
        strand = str(f.parent)[-1]
        # Feature counts may have extra columns (not just a Series),
        # the count is the last columns though. So,
        # FeatureCounts(f).df[df.columns[-1]] is a time series
        df = FeatureCount(f).df
        df = df[df.columns[-1]]
        res_dict[strand] = int(df.sum())

    strandness = res_dict["1"] / (res_dict["1"] + res_dict["2"])
    res_dict["strandness"] = strandness

    if strandness < tolerance:
        res_dict["strand"] = 2
    elif strandness > 1 - tolerance:
        res_dict["strand"] = 1
    elif 0.5 - tolerance < strandness and strandness < 0.5 + tolerance:
        res_dict["strand"] = 0
    else:
        res_dict["strand"] = None

    df = pd.DataFrame(res_dict, index=[sample_name])

    return df


def get_most_probable_strand_consensus(rnaseq_folder, tolerance):
    """From a sequana rna-seq run folder get the most probable strand, based on the
    frequecies of counts assigned with '0', '1' or '2' type strandness
    (featureCounts nomenclature)

    If guess is not possible given the tolerance, fills with None
    """

    rnaseq_folder = Path(rnaseq_folder)
    sample_folders = list(
        set([x.parent for x in rnaseq_folder.glob("*/feature_counts_[012]")])
    )

    df = pd.concat(
        [
            get_most_probable_strand(sample_folder, tolerance)
            for sample_folder in sample_folders
        ]
    )
    df = df[['0','1','2', 'strandness', 'strand']]

    logger.info(f"Strand guessing for each files (tolerance: {tolerance}):\n")
    logger.info(df)

    try:
        most_probable = df['strand'].value_counts().idxmax()
    except:
        # if all events are None, return -1
        most_probable = -1

    return most_probable, df


class MultiFeatureCount():
    # USED in rnaseq pipeline

    def __init__(self, rnaseq_folder='.', tolerance=0.1):
        self.tolerance = tolerance
        self.rnaseq_folder = rnaseq_folder

    def get_most_probable_strand_consensus(self):
        most_probable, df = get_most_probable_strand_consensus(
            self.rnaseq_folder,
            self.tolerance)
        return most_probable, df

    def plot_strandness(self, fontsize=12, output_filename='strand_summary.png',
        savefig=False):
        # USED in rnaseq pipeline
        most_probable, df = self.get_most_probable_strand_consensus()

        df = df.sort_index(ascending=False)
        df['strandness'] = df['strandness'].T
        df['strandness'].plot( kind='barh')
        pylab.xlim([0, 1])
        pylab.grid(True)
        pylab.axvline(self.tolerance, ls='--', color='r')
        pylab.axvline(1-self.tolerance, ls='--', color='r')
        pylab.axvline(0.5, ls='--', color='k')
        pylab.xlabel("Strandness", fontsize=fontsize)
        pylab.tight_layout()
        if savefig: #pragma: no cover
            pylab.savefig(output_filename)


class FeatureCount:
    """Read a featureCounts output file.

    #TODO: Test on single and multi featurecounts files and see how self.df and
    self.rnadiff_ready_df behave.
    """

    def __init__(
        self,
        filename,
        clean_sample_names=True,
        extra_name_rm=["_Aligned"],
        drop_loc=True,
        rnadiff_ready=True,
    ):
        """.. rubric:: Constructor

        Get the featureCounts output as a pandas DataFrame
        :param bool clean_sample_names: if simplifying the sample names in featureCount output columns
        - extra_name_rm: extra list of regex to remove from samples_names (ignored if clean_sample_name is False)
        - drop_loc: if dropping the extra location columns (ie getting only the count matrix)
        """

        if not Path(filename).exists(): # pragma: no cover
            raise IOError(f"No file found with path: {filename}")

        self.filename = filename
        self.clean_sample_names = clean_sample_names
        self.extra_name_rm = extra_name_rm
        self.drop_loc = drop_loc
        self._df = self._get_df()
        # Count matrix prepared for rnadiff
        if rnadiff_ready:
            self.rnadiff_ready_df = self._get_rnadiff_ready_df()
            self.target_df = self._get_target_df()

    def _get_rnadiff_ready_df(self):
        """Prepare a count matrix from a multi-sample featureCount file.

        This is in particular add a 'rawCounts_' to column names to not have an
        import problem in R with labels starting with numbers
        """
        df = pd.read_csv(self.filename, sep="\t", comment="#", index_col=0)
        df.drop(["Chr", "Start", "End", "Strand", "Length"], axis=1, inplace=True)
        df.columns = [
            self._clean_sample_names(x, self.extra_name_rm) for x in df.columns
        ]
        df.set_index(df.columns[0], inplace=True)
        return df

    def _get_target_df(self):
        """ Prepare the table with grouping information for rnadiff
        """
        df = pd.DataFrame(
            {
                "sample": self.rnadiff_ready_df.columns,
                "label": self.rnadiff_ready_df.columns.str.replace("rawCounts_", ""),
                "condition": None,
            }
        )
        df.set_index(df.columns[0], inplace=True)
        return df

    def _get_df(self):

        df = pd.read_csv(self.filename, sep="\t", comment="#", index_col=0)

        if self.drop_loc:
            df.drop(["Chr", "Start", "End", "Strand", "Length"], axis=1, inplace=True)

        if self.clean_sample_names:
            df.columns = [
                self._clean_sample_names(x, self.extra_name_rm) for x in df.columns
            ]
        return df

    df = property(_get_df)

    def _clean_sample_names(self, sample_path, extra_name_rm):
        """ Clean sample names in feature count tables """

        new_name = str(Path(sample_path).stem)
        new_name = new_name.split(".")[0]

        for pattern in extra_name_rm:
            new_name = re.sub(pattern, "", new_name)

        return new_name


