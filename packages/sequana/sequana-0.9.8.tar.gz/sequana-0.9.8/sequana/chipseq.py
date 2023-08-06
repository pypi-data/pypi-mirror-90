


from sequana.lazy import pandas as pd
from sequana.lazy import pylab
from sequana.lazy import numpy as np
from sequana import logger





class PhantomPeaks():
    """Manipulate output of PhantomPeaks


1_S1_L001.sorted.bam	3534910	150,250,275	0.97029159945329,0.968713084636106,0.968468832890883	80	0.9682
442	1500	0.9669921	1.003412	2.6352	2

    The metrics file is tabulated

    * Filename
    * numReads: effective sequencing depth i.e. total number of mapped reads in the input file
    * estFragLen: comma separated strand cross-correlation peak(s) in decreasing order of correlation. In almost all cases, the top (rst) value in the list represents the predominant fragment length.
    * corr estFragLen: comma separated strand cross-correlation value(s) in decreasing order (col3 follows the same order)
    * phantomPeak: Read length/phantom peak strand shift
    * corr phantomPeak: Correlation value at phantom peak
    * argmin corr: strand shift at which cross-correlation is lowest
    * min corr: minimum value of cross-correlation
    * Normalized strand cross-correlation coecient (NSC) = COL4 / COL8. ;1=no
enrichment. NSC >1.1 is good
    * Relative strand cross-correlation coecient (RSC) = (COL4 - COL8) / (COL6 -
COL8); RSC=0 means no signal, <1 low quality and >1 means high enrichment.
should aim at RSC>0.8
    *  QualityTag: Quality tag based on thresholded RSC (codes: -2:veryLow; -1:Low; 0:Medium; 1:High; 2:veryHigh)

    """
    def __init__(self, filename):
        self.df = pd.read_csv(filename, sep='\t', header=None)
        self.df.columns = ['filename', 'num_reads', 'estimated_fragment_length',
            'corr', 'phantom_peak', 'corr_phantom_peak', 'argmin_corr',
'min_corr', 'NSC',
            'RSC', 'quality_tag']

    def read(self, filename):
        df = pd.read_csv(filename, sep='\t', header=None)
        df.columns = ['filename', 'num_reads', 'estimated_fragment_length',
            'corr', 'phantom_peak', 'corr_phantom_peak', 'argmin_corr',
'min_corr', 'NSC',
            'RSC', 'quality_tag']
        self.df = self.df.append(df)
        self.df.reset_index(inplace=True, drop=True)

    def plot_RSC(self):
        self.df.RSC.plot(kind='bar')
        pylab.axhline(0.8, lw=2, color='r', ls='--')




class Phantom():
    """

    prints
    - the reference chromosome, 
    - the starting position-1
    - position -1 + sequence length
    - N
    - 1000
    - + if flag is 16 (or equivalent) otherwise prints -


    c = Phantom()
    c.chromosomes
    data = c.get_data('NC_002506.1')
    mask = c.remove_anomalies(data)
    data = data[mask]
    c.scc(data)

    # Note that binning is set to 5 by default so this will comput from -500 to
    # 500
    X = range(-100,100)
    Y = [c.cor(x) for x in X]
    plot([x*5 for x in X], Y)


     c = chipseq.Phantom(binning=10, start=-500, stop=500)
    c.read_align("test.align")
    results, df = c.run()
    c.stats(results, df)



    """
    def __init__(self, bamfile=None, binning=5, start=-500, stop=1500):

        self.start = start
        self.stop = stop
        self.binning = binning


        cmd = """
        samtools view -F 0x0204 -o | awk 'BEGIN{FS="\t";OFS="\t"} {if (and($2,16) > 0) {print $3,($4-1),($4-1+length($10)),"N","1000","-"} else {print $3,($4-1),($4-1+length($10)),"N","1000","+"}}' - > test.align
        """
        #shell(cmd)
        self.df = None

    def read_align(self, readfile):

        self.df = pd.read_csv(readfile, sep='\t', header=None)
        self.df.columns = ['ref', 'start','end', 'dummy', 'quality', 'strand']
        from pylab import median
        self.read_length = round(median(self.df['end']-self.df['start']))
        self.chromosomes = self.df['ref'].unique()

    def run(self):
        if self.df is None:
            print("call read_align() method to read alignement file")
            return
        m = int(self.start / self.binning)
        M = int(self.stop / self.binning)
        results = {}
        # because bins is set to 5, we actually go from m*5 to M*5
        X = range(m, M+1, 1)
        Xreal = np.array(range(m*self.binning, (M+1)*self.binning, self.binning))

        for chrom in self.chromosomes:
            logger.info("Processing {}".format(chrom))
            data = self.get_data(chrom)
            L = len(data)
            self.scc(data)

            # shift correlation
            Y = [self.cor(x) for x in X] 
            results[chrom] = {'data_length': L, 'Y': np.array(Y), 'X': Xreal}

        # weighted average usng orginal length of the chrmosomes
        weights = np.array([results[x]['data_length'] for x in self.chromosomes])
        weights = weights / sum(weights)

        self.results = results
        self.weights = weights
        # now the weighted cross correlation
        df_avc = pd.DataFrame([w* results[x]['Y'] for w,x in zip(weights, self.chromosomes)])
        df_avc = df_avc.T
        df_avc.index = Xreal
        return results, df_avc

    def stats(self, results, df_avc, bw=1):
        # average cross correlation across all chromosomes
        print("Read {} fragments".format(len(self.df)))
        print("ChIP data mean length: {}".format(self.read_length))
        #df_avc.sum(axis=1).plot()
        df = df_avc.sum(axis=1)
        corr_max = df.max()
        shift_max = df.idxmax()
        # note that in phantomPeak, they use the last value as min... not the
        # actual min. Not very important.
        corr_min = df.min()
        shift_min = df.idxmin()
        print("Maximum cross-correlation value: {:.5f}".format(corr_max))
        print("Maximum cross-correlation shift: {}".format(shift_max))
        print("Minimum cross-correlation value: {:.5f}".format(corr_min))
        print("Minimum cross-correlation shift: {}".format(shift_min))

        # original code phantomPeak but always equal to 1 it range max >5 ??
        # default is 500 so sbw=1 whatsoever
        #sbw = 2 * floor(ceil(5/15000) / 2) + 1
        sbw = 1

        # here we could use a rolling mean 
        #df.rolling(window=5, center=True).mean()

        # so following runnin mean is useless
        # cc$y <- runmean(cc$y,sbw,alg="fast")
        # 
 
        # again, computation of bw but always equal to 1 ....
        # Compute cross-correlation peak
        #  bw <- ceiling(2/iparams$sep.range[2]) # crosscorr[i] is compared to crosscorr[i+/-bw] to find peaks
        #bw = 1
        # search for local peaks within bandwidth of bw = 1 
        peakidx = df.diff(periods=bw) >0
        peakidx = peakidx.astype(int).diff(periods=bw)==-1

        # the final bw points are NA and filled with False
        peakidx = peakidx.shift(-bw).fillna(False)


        df_peaks = df[peakidx]
        # when searching for max, exclude peaks from the excluded region
        exclusion_range = [10, self.read_length + 10 ]
        mask = np.logical_or(df_peaks.index<exclusion_range[0],
                            df_peaks.index>exclusion_range[1])
        df_peaks = df_peaks[mask]

        #
        max_peak = df_peaks.max()
        shift_peak = df_peaks.idxmax()

        # now, we select peaks that are at least 90% of main peak and with shift
        # higher than main shift. why higher ?
        mask = np.logical_and(df_peaks > max_peak * 0.9, df_peaks.index >= shift_peak)
        best_df_peaks = df_peaks[mask]
        best = best_df_peaks.sort_values(ascending=False)[0:3]

        values = ",".join(["{:.5f}".format(x) for x in best.values])
        pos = ",".join([str(x) for x in best.index])
        print("Top 3 cross-correlation values: {}".format(values))
        print("Top 3 estimates for fragment length: {}".format(pos))


        # now the real window half size according to phantom peaks, not spp ...
        # min + (max-min)/3
        threshold = (df_peaks.max() - corr_min)/3 + corr_min
        whs = df[df>threshold].index.max()


        # coming back to real cross correlation, identify peak in window
        # readlength +- 2*binning  !! not symmetry in phantompeak
        # x >= ( chip.data$read.length - round(2*binning) & 
        # x <= ( chip.data$read.length + round(1.5*binning) 

        binning = self.binning
        ph_min = self.read_length - round(2*binning)
        ph_max = self.read_length + round(1.5*binning)
        phantom = df[np.logical_and(df.index >=ph_min, df.index<= ph_max)]
        print("Phantom peak range detection:{}-{}".format(ph_min, ph_max))
        print("Phantom peak location:{}".format(phantom.idxmax()))
        print("Phantom peak Correlation: {:.5f}".format(phantom.max()))

        NSC = df_peaks.max() /  phantom.max()
        # error in phatompeaks ?? is encoded as follows but no link with phantom
        # peak...
        # Another difference with phantom peak is that the min in phantom peak
        # is not the min but last value on the RHS so 
        #    phantom_coeff = df_peaks.max() /  df.min()
        # is 
        #    phantom_coeff = df_peaks.max() /  df.iloc[-1]
        NSC_spp = df_peaks.max() / df.iloc[-1]
        print("Normalized Strand cross-correlation coefficient (NSC): {:.5f} [{:.5f}]".format(NSC, NSC_spp))
        RSC = (df_peaks.max() - df.min()) / (phantom.max() - df.min())
        RSC_spp = (df_peaks.max() - df.iloc[-1]) / (phantom.max() - df.iloc[-1])
        print("Relative Strand cross-correlation Coefficient (RSC): {:.5f} [{:.5f}]".format(RSC, RSC_spp))

        if RSC >0 and RSC < 0.25:
            tag = -2
        elif RSC >=0.25 and RSC <0.5:
            tag = -1
        elif RSC >=0.5 and RSC <1:
            tag = 0
        elif RSC >=1 and RSC <1.5:
            tag = 1
        elif RSC >=1.5 :
            tag =  2
        print("Phantom Peak Quality Tag: {}".format(tag))

        pylab.clf()
        df.plot()
        ##df_peaks.plot(marker="o", lw=0)
        ylim = pylab.ylim();
        #pylab.axvline(whs, ls='--', color='k', lw=1)
        Y0,Y1 = pylab.ylim()
        pylab.plot([phantom.idxmax(), phantom.idxmax()], [Y0, phantom.max()],  ls='--', color='k', lw=1)
        pylab.plot([df.idxmax(), df.idxmax()], [Y0, df.max()], ls='--', color='r', lw=2)
        #pylab.fill_betweenx(ylim, 10,85, color='grey', alpha=0.5)
        pylab.ylim(ylim)
        pylab.ylabel("Cross-correlation")
        pylab.xlabel("strand-shift: {}bp\nNSC={:.5f}, RSC={:.5f}, Qtag={}".format(
            best.index[0], NSC, RSC, tag)) 
        pylab.xlim(self.start, self.stop)
        pylab.grid(True, zorder=-20)
        try:
            pylab.tight_layout()
        except:
            pass
        results = {'NSC': NSC ,'RSC': RSC, 'Qtag': tag}
        return results

    def get_data(self, chrname, remove_anomalies=True):


        df = self.df.query('ref==@chrname')

        # first the fragment position, shifting - strand by fragment length
        data = np.array([x if z=='+' else -y for x,y,z in zip(df['start'], df['end'], df['strand'])])

        # sort by absolute position
        res = pd.DataFrame(data)
        res.columns = ['x']
        res['abs'] = res['x'].abs()
        res = res.sort_values('abs')
        del res['abs']

        if remove_anomalies:
            mask = self.remove_anomalies(res)
            res = res[mask]

        return res


    def remove_anomalies(self, data, bin=1, trim_fraction=1e-3,z=5,
        return_indecies=False):

        zo = z*3

        x = data['x']

        from numpy import floor, ceil, sqrt
        # the frequencies, sorted from smaller to larger
        tt = floor(x / bin).value_counts().sort_values()
        #print(len(tt))

        # sort and select first 99.9%
        # floor to agree with phantom
        stt = tt.iloc[0:int(floor(len(tt)*(1-trim_fraction)))]
        #print(len(stt))

        #print(stt.sum())
        mtc = stt.mean()
        var_base = 0.1
        tcd = sqrt(stt.var()+var_base)

        thr = max(1, ceil(mtc+z*tcd))
        thr_o = max(1,ceil(mtc+zo*tcd))

        # filter tt
        tt = tt[tt>thr]
        #print("tp2 length={}".format(len(tt)))

        #print(tcd, mtc, thr, thr_o)
        # get + and - tags
        tp = tt.index
        #<- as.numeric(names(tt2));

        pti = set(tp[tp>0])
        pti2 = set([-x for x in tp[tp<0]])
        it = pti.intersection(pti2)
        #print("length it {}".format(len(it)))
        #print(it)
        #it <- intersect(tp[pti],(-1)*tp[!pti]);
        # add one-strand matches
        #it <- unique(c(it,tp[tt>thr.o]));

        it = sorted(it.union(set(tt[tt>thr_o].index)))
        #print(len(it), sum(it))

        #sit <- c(it,(-1)*it);
        #sit =  [-x for x in it] + list(it)
        sit =  list(it)[::-1] + [-x for x in list(it)[::-1]]
        #print(len(sit), sum(sit))

        if(bin>1):
            # From 0 to 5+1 to agree with phantom R code
            sit = sorted([x*5+y for y in range(0,6) for x in sit])

        #sit = set([int(x) for x in sit])
        #print(len(sit), sum(sit))
        #if return_indecies:
        #    return 
        #  return(!tv %in% sit);
        # else :
        # return(tv[!tv %in% sit]);

        sit = set(sit)
        return [False if x in sit else True for x in data['x']]

    def scc(self, data, llim=10):

        tt = (np.sign(data['x']) * np.floor(data['x'].abs() / self.binning +0.5)).value_counts()

        mu = tt.mean()
        tt = tt[tt<llim*mu]
        #
        tc = tt.index

        pdata = tt[tc>0]
        ndata = tt[tc<0]

        ntv = ndata.values
        ptv = pdata.values

        self.pdata= pdata
        self.ndata= ndata
        r1 = min(-1*ndata.index.max(), pdata.index.min())
        r2 = max(-1*ndata.index.min(), pdata.index.max())
        l = r2 - r1+1
        self.L = l
        mp = ptv.sum() * self.binning / l
        mn = ntv.sum() * self.binning / l
        ptv = ptv - mp
        ntv = ntv - mn
        self.mp = mp
        self.mn = mn
        ntc = -tt.index[[True if x<0 else False for x in tt.index]].values
        ptc = tt.index[[True if x>0 else False for x in tt.index]].values

        self.ntc = ntc
        self.ptc = ptc

        self.ntv = ntv
        self.ptv = ptv
        from numpy import sqrt
        ss = sqrt((sum(ptv**2)+(l-len(ptv))*mp**2) * (sum(ntv**2)+(l-len(ntv))*mn**2))
        self.ss = ss
        self.nn = pd.DataFrame(self.ntv, index=self.ntc)

        logger.info("mp={}; mn={}, ss={}".format(self.mp, self.mn, self.ss))
        logger.info("ptv sum={}; ptv len ={}, ntv sum={} ntv len {}".format(
            sum(self.ptv), len(self.ptv), sum(self.ntv), len(self.ntv)))
        logger.info("ptc sum={}; ptc len ={}, ntc sum={} ntc len {}".format(
            sum(self.ptc), len(self.ptc), sum(self.ntc), len(self.ntc)))

    def cor(self, s):
        logger.info("shift {}".format(s))
        p = pd.DataFrame(self.ptv, index=self.ptc + s)
        n = self.nn

        self.X = p[p.index.isin(n.index)]
        self.compX = p[p.index.isin(n.index)==False]
        self.Y = n[n.index.isin(p.index)]
        self.compY = n[n.index.isin(p.index)==False]

        R = self.L - len(self.ptv) - len(self.ntc) + len(self.X)

        #print(len(self.X), len(self.Y))
        #print( (self.X * self.Y).sum()[0] )
        #print(self.compX.sum()[0] * self.mn )
        #print(self.compY.sum()[0]*self.mp)
        XY = (self.X * self.Y).sum()[0] 
        XX = (self.compX.sum()[0] * self.mn)
        YY = (self.compY.sum()[0] * self.mp)
        corr =  (XY - XX - YY + self.mp*self.mn*R)/self.ss 
        return corr



