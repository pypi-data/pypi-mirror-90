# -*- coding: utf-8 -*-
#
#  This file is part of Sequana software
#
#  Copyright (c) 2018 - Sequana Development Team
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
"IEM class"
import sys
import collections
from sequana import logger
logger.name = __name__


__all__ = ["IEM"]


class IEM():
    """!! In progress to replace some of the adapters module classes

    Simple IEM file parser.

    commas are used as delimiter between adajacent fields on the same line
    If a field contains a comma, use double quotes.
    If a field contains double quote, the field needs to be wrapped in double
    quotes.

    Example::

        This is in "quotes", as well as commas

    is represented in the Sample Sheet as::

        "This is in ""quotes"", as well as commas"

    There is no minimum or maximum comma delimiters required on each line.

    The end of the line can be padded with as many commas as desired, which are ignored.

    Empty lines are ignored. Lines made of commas and/or white spaces only are ignored.

    Sections are case-sensitive and denoted by a line starting and ending with square
    brackets. Except for commas and end of line, no extra character after the
    ending square bracket are authorise.


    Sample sheet must begin with the [Header] section and end with the [Data]
    section. Others can be ordered arbitraly.

    **Header** section must be on the first line. It contains records represented
    as a series of key-value pairs. So, each line requires exactly two fields.

    **Settings** is an optional section with key-value pairs.

    **Reads** contains number of cycles per read. Only required for MiSeq.

    For adapters IEM sample sheet those fields are known to be present:
    [Version], [Name], [settings], [I7], [I5], [IndexPlateLayout].


    **Data** section: it is required and must be located at the end of the
    Sample Sheet file. The Data section is a CSV-like table.

    No specific ordering of the column names is required and they are
    not case-sensitive. At a minimum, the one column that is universally
    required is Sample_ID, which provides a unique string identifier
    for each sample.

    Example of typical Data section to be used with bcl2fastq::

        [Data]
        Sample_ID,Sample_Name,I7_Index_ID,index,I5_INdex_ID,index2
        A10001,Sample_A,D701,AATACTCG,D501,TATAGCCT
        A10002,Sample_B,D702,TCCGGAGA,D501,TATAGCCT
        A10003,Sample_C,D703,CGCTCATT,D501,TATAGCCT
        A10004,Sample_D,D704,GAGATTCC,D501,TATAGCCT

    :references: illumina specifications 970-2017-004.pdf
    """

    def __init__(self, filename, tryme=False):
        self.filename = filename
        if tryme:
            try:self._scanner()
            except:pass
        else:
            self._scanner()

    def _line_cleaner(self, line, line_count):
        # We can get rid of EOL and spaces
        line = line.strip()

        # is it an empty line ?
        if len(line) == 0:
            return line

        # if we are dealing with a section title, we can cleanup the
        # line. A section must start with '[' and ends with ']' but
        # there could be spaces and commands.
        if line.startswith('['):
            #[Header], ,, ,\n becomes [Header]
            line = line.strip(", ") # note the space AND comma
            if line.endswith("]") is False:
                raise ValueError("Found incorrect syntax on line {}: {}. Maybe an extra character such as ; ".format(line_count, line))

        return line

    def _scanner(self):

        current_section = None
        data = collections.defaultdict(list)
        with open(self.filename, "r") as fin:
            for line_count, line in enumerate(fin.readlines()):
                line = self._line_cleaner(line, line_count+1)
                if len(line) == 0:
                    continue
                if line.startswith("[") and line.endswith("]"):
                    name = line.lstrip("[").rstrip("]")
                    current_section = name
                else:
                    data[current_section] += [line]

        if "Header" not in data.keys(): #pragma: no cover
            logger.warning("Input file must contain [Header]")

        if "Data" not in data.keys(): #pragma: no cover
            logger.warning("Input file must contain [Data]")
        self.data = data

    def _get_df(self):
        import pandas as pd
        import io
        df = pd.read_csv(io.StringIO("\n".join(self.data['Data'])))
        if len(df.columns)==0:
            raise ValueError("Invalid sample sheet in the Data section")
        return df
    df = property(_get_df)

    def validate(self):
        """This method checks whether the sample sheet is correctly formatted

        Checks for:
            * presence of ; at the end of lines indicated an edition with excel that
              wrongly transformed the data into a pure CSV file
            * inconsistent numbers of columns in the [DATA] section, which must be
              CSV-like section
            * Extra lines at the end are ignored

        """
        # could use logger, but simpler for now
        # Note that this code is part of sequana_demultiplex
        prefix = "ERROR  [sequana_pipelines.demultiplex.check_samplesheet]: "
        try:
            with open(self.filename, "r") as fp:
                line = fp.readline()
                cnt = 1
                if line.rstrip().endswith(";") or line.rstrip().endswith(","): #pragma: no cover
                    sys.exit(prefix + "Unexpected ; or , found at the end of line {} (and possibly others). Please use IEM  to format your SampleSheet. Try sequana_fix_samplesheet for extra ; or , ".format(cnt))

                while line:
                    line = fp.readline()
                    cnt += 1
                    if "[Data]" in line:
                        line = fp.readline()
                        cnt += 1
                        if len(line.split(',')) < 2 or "Sample" not in line: #pragma:  no cover
                            sys.exit(prefix + ": No header found after [DATA] section")
                        nb_col = len(line.split(','))
                        # now we read the first line below [Data]
                        line = fp.readline()
                        cnt += 1
                        while line:
                            if line.strip() and len(line.split(',')) != nb_col:
                                sys.exit(prefix + "Different number of column in [DATA] section on line: "+str(cnt))
                            line = fp.readline()
                            cnt += 1
        except Exception as e: #pragma: no cover
            raise ValueError("type error: " + str(e))
        return 0


    def _get_settings(self):
        data = {}
        for line in self.data['Settings']:
            key, value = line.split(",")
            data[key] = value
        return data
    settings = property(_get_settings)


    def _get_header(self):
        data = {}
        for line in self.data['Header']:
            key, value = line.split(",")
            data[key] = value
        return data
    header =  property(_get_header)

    def _get_name(self):
        if len(self.data['Name']) == 1:
            return self.data['Name'][0]
        else:
            return self.data['Name']
    name = property(_get_name)

    def to_fasta(self, adapter_name=""):
        ar1 = self.settings['Adapter']
        try:ar2 = self.settings['AdapterRead2']
        except: ar2 =""

        for name, index in zip(self.df['I7_Index_ID'], self.df['index']):
            read = "{}{}{}".format(ar1, index, ar2)
            frmt = {"adapter": adapter_name, "name": name, "index": index}
            print(">{adapter}_index_{name}|name:{name}|seq:{index}".format(**frmt))
            print(read)

        if 'index2' in self.df.columns:
            for name, index in zip(self.df["I5_Index_ID"], self.df['index2']):
                read = "{}{}{}".format(ar1, index, ar2)
                frmt = {"adapter": adapter_name, "name": name, "index": index}
                print(">{adapter}_index_{name}|name:{name}|seq:{index}".format(**frmt))
                print(read)

    def quick_fix(self, output_filename):

        found_data = False
        with open(self.filename) as fin:
             with open(output_filename, "w") as fout:
                 for line in fin.readlines():

                     if line.startswith('[Data]'):
                         found_data = True
                    
                     if found_data:
                         line = line.replace(";", ",")
                     else:
                         line = line.strip().rstrip(";")
                         line = line.replace(";", ",")
                         line = line.strip().rstrip(",")
                     fout.write(line.strip("\n")+"\n")

