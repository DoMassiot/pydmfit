# Dominique Massiot
# CEMHTI-CNRS
# personnal web page : http://www.cemhti.cnrs-orleans.fr/?nom=massiot
# dmfit program : http://nmr.cemhti.cnrs-orleans.fr/Default.aspx

# view the log files of dmfit
# you have to initialize tmpdir variable to your temp directory...

from dmfit_utils import fileUtils as file
import os
import matplotlib.pyplot as plt
import math
import numpy as np
import scipy.stats as stats

class logMultiFile:

    def __init__(self, path=None):
        self.path = None
        self.values = []
        self.names = None
        self.multiResults = []
        if path:
            self.loadFromFile(path)

    def analyseLine(self, line):
        print (line)

    def analyseResult(self, result):
        resultDict = {}
        for r in result[2::]:
            if r[0].isnumeric():
                self.analyseLine(r)
            else:
                print ("no value : ", r)
        return resultDict.multiResults.append()

    def loadFromFile(self, path):
        if path:
            self.path = path
        print(f"getting Monte Carlo dmfit output '{os.path.split(self.path)[-1]}'")
        lines = file.getLines_from_file(path, clean=True)
        if not lines:
            return
        print("----------------------")
        multiResults = []
        nmulti = 0
        multilines = []
        for l in lines:
            print(l)
            if l.find("------ Begin FitMultiple ------")>=0:
                if nmulti > 0:
                    multiResults.append(multilines)
                    multilines = []
                nmulti += 1
            else:
                if nmulti > 0:
                    if len(l) > 0:
                        multilines.append(l)
        if nmulti > 0:
            multiResults.append(multilines)
            print (f"found {nmulti} multiple fits")
#            print (self.multiResults)
            n = 0
            for m in multiResults:
                print(f"results#{n}:")
                self.analyseResult(m)
                n += 1
        print("----------------------")


    @property
    def ncol(self):
        return len(self.names) if self.names else 0

    def getFromFile(self, path):
        if path:
            self.path = path
        print(f"getting Monte Carlo dmfit output '{os.path.split(self.path)[-1]}'")
        lines = file.getLines_from_file(path, clean=True)
        if not lines:
            print("failed to load - aborted")
            self.path = None
            return False
        self.path = path
        self.names = lines[0].split("\t")
        self.values = []
        print (f"{self.ncol-1} parameters found : {self.names[1::]}")
        for l in lines:
            try:
                trow = l.split("\t")
                row = [float(v) for v in trow]
                self.values.append(row)
#                print (row)
            except:
                pass
        if not self.values == []:
            print(f"{len(self.values)} fit found")
        print(f"Monte Carlo error file '{self.path}' loaded...")
        for i in range(1, self.ncol):
            t = [r[i] for r in self.values]
            self.dataDict.update({self.names[i]: t})
        self.analyse()
        return True
    def __repr__(self):
        rep=[f"Monte Carlo error report for '{os.path.split(self.path)[-1]}'"]
        rep.append(f"{len(self.dataDict)} parameters and {len(self.values)} steps")
        self.errorDict={}
        for d in self.dataDict:
            avg = np.average(self.dataDict[d])
            sdev = math.sqrt(np.var(self.dataDict[d]))
            self.errorDict.update({d:(avg, sdev)})
            rep.append (f"{d}:\t{avg:0.2f} +/- sdev:{sdev:0.4g} - {sdev/avg*100:0.2f}%")
        return "\n".join(rep)

    def analyse(self):
        print (self)

    @property
    def imagepath(self):
        return os.path.splitext(self.path)[0] + ".png"

    @property
    def reportpath(self):
        return self.path+ ".report"

    def saveReportToFile(self):
        link = f"http://nmr.cemhti.cnrs-orleans.fr/temp/{os.path.split(self.imagepath)[-1]}"
        rep = f"<hr><a href='{link}'><div class='right' ><img src='{link}' width='400px' /></div></a>" + self.__repr__()+"\n"
        file.writeToFile(self.reportpath, rep)

    def plotHistogram(self, n):
        if n in self.dataDict.keys():
            nn, bins, patches = plt.hist(self.dataDict[n], bins=20) #, normed=1)
            # add a 'best fit' line
            avg, sdev = self.errorDict[n]
            y = stats.norm.pdf(bins, avg, sdev)
            y = y/max(y)*max(nn)
            plt.plot(bins, y, 'r--')
            plt.title(f"{n}\n{avg:0.3f} +/- {sdev:0.4g} - {sdev/avg*100:0.2f}%")

    def histograms(self, show=False):
        plt.figure()
        l = len(self.dataDict)
        if l<=4:
            nrow, ncol, ftsize = (2, 2, 10)
        elif l <= 9:
            nrow, ncol, ftsize = (3, 3, 8)
        elif l <= 16:
            nrow, ncol, ftsize = (4, 4, 6)
        elif l <= 25:
            nrow, ncol, ftsize = (5, 5, 5)
        elif l<=30:
            nrow, ncol, ftsize = (6, 5, 5)
        else:
            nrow, ncol, ftsize = (6, 6, 5)
        n = 0
        nmod = nrow*ncol
        for d in self.dataDict:
            fig = plt.subplot(nrow, ncol, n+1)
            plt.subplots_adjust(wspace=0.1, hspace=0.65)
            try:
                pass
            except:
                pass
            self.plotHistogram(d)
            fig.yaxis.set_visible(False)
            fig.xaxis.set_visible(False)
            for item in ([fig.title, fig.xaxis.label, fig.yaxis.label] + fig.get_xticklabels() + fig.get_yticklabels()):
                item.set_fontsize(ftsize)
            n += 1
            if n==nmod:
                if show:
                    plt.show()
                else:
                    plt.savefig(self.imagepath)
                    print (f"figure saved in '{self.imagepath}'")
                    return
                n=0
        if not n==nmod:
            if show:
                plt.show()
            else:
                plt.savefig(self.imagepath)
                print(f"figure saved in '{self.imagepath}'")
                return

if __name__ == "__main__":
    # for testing purpose- provide here your temp directory...
    tmpdir = "give here the directory of dmfit log files (temp directory by default)"
    files = {"multi": tmpdir+"dmfit_multi.log",
             "compute": tmpdir+"dmfit-compute.log",
             "dmfit":  tmpdir+"dmfit.log"}

    while True:
        print ("======================")
        print (f"current dmfit log files directory (temp dir): '{file.currentDirectory()}'")
        rep = input(f"files.keys() - d)mfit.log, m)ulti.log c)ompute.log q)uit\nmake your choice ? ").lower()
        if rep.startswith("q"):
            exit(0)
        elif rep.startswith("d"):
            logMultiFile(files["dmfit"])
        elif rep.startswith("c"):
            logMultiFile(files["compute"])
        elif rep.startswith("m"):
            logMultiFile(files["multi"])
        else:
            print (f"?? unknown choice {rep} ??")

