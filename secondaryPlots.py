from .viewHelper import *


SecondaryPlots = [{"name":"completed","en_name":"Completed Secondary","sp_name":"Secundaria Completa","pk":1},
                 {"name":"incompleted","en_name":"Completed and Incompleted Secondary","sp_name":"Secundaria Completa e Incompleta","pk":2}]

###################################################################################
# Secondary Schooling
#
#

def GetBarroLeeSecCompleted(lang, female=False):
    en = ""
    sp = ""
    if female:
        en = "Female"
        sp = "femenina"

    p1 = Plot( Text("Share","Porcentaje") , Text(en + " Population with completed secondary","Poblacion " +sp + "con escuela secundaria completa"), Text("Share","Porcentaje")) 
    tot = AddBarroLeeDataToPlotDecades(p1, lang, "SEC.CMPT", female)
    if (tot <= 3): p1.setType("P")
    return p1


def GetBarroLeeSecInCompleted(lang, female=False):
    en = ""
    sp = ""
    if female:
        en = "Female"
        sp = "femenina"

    p1 = Plot( Text("Share","Porcentaje") , Text(en + " Population with (in)completed secondary","Poblacion " +sp + "con escuela secundaria (in)completa"), Text("Share","Porcentaje")) 
    tot = AddBarroLeeDataToPlotDecades(p1, lang, "SEC.ICMP", female)
    if (tot <= 3): p1.setType("P")
    return p1


def GetSecondaryCompletionPlots(lang):
    plots= []
    plots.append(GetBarroLeeSecCompleted(lang).getPlotDict(lang))
    plots.append(GetBarroLeeSecCompleted(lang, True).getPlotDict(lang))
    return plots

def GetSecondaryInCompletionPlots(lang):
    plots= []
    plots.append(GetBarroLeeSecInCompleted(lang).getPlotDict(lang))
    plots.append(GetBarroLeeSecInCompleted(lang, True).getPlotDict(lang))
    return plots


def SecondarySchoolingIndicatorsNames():
    plot_indicators = []
    plot_indicators.extend(GetListOfBarroLeeIndicators("SEC.CMPT"))
    plot_indicators.extend(GetListOfBarroLeeIndicators("SEC.CMPT", True))
    plot_indicators.extend(GetListOfBarroLeeIndicators("SEC.ICMP"))
    plot_indicators.extend(GetListOfBarroLeeIndicators("SEC.ICMP", True))

    return plot_indicators

