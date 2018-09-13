# Dominique Massiot
# CEMHTI-CNRS
# personnal web page : http://www.cemhti.cnrs-orleans.fr/?nom=massiot
# dmfit program : http://nmr.cemhti.cnrs-orleans.fr/Default.aspx

# script called on dmfit web page

import sys
from dmfit_utils import errorsMonteCarlo as mc

print (sys.argv)

usage = "usage : python errorDmfit xxxMonteCarlo.txt"

if len(sys.argv) > 1:
    path = sys.argv[1]
    MC = mc.errorMonteCarlo(path)
    MC.saveReportToFile()
    MC.histograms()
else:
    print("no command line parameters found")
    print(usage)

