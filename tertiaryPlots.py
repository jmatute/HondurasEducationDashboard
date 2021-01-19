from .viewHelper import *


TertiaryPlots = [{"name":"completed","en_name":"Completed Tertiary","sp_name":"Educacion Terciaria Completa","pk":1},
                 {"name":"incompleted","en_name":"Completed and Incompleted Tertiary","sp_name":"Educacion Terciaria Completa e Incompleta","pk":2}]

###################################################################################
# Tertiary Schooling
#
#

def GetBarroLeeTerCompleted(lang, female=False):
    en = ""
    sp = ""
    if female:
        en = "Female"
        sp = "femenina"

    p1 = Plot( Text("Share","Porcentaje") , Text(en + " Population with completed tertiary","Poblacion " +sp + "con educacion terciaria completa"), Text("Share","Porcentaje")) 
    tot = AddBarroLeeDataToPlotDecades(p1, lang, "TER.CMPT", female)
    if (tot <= 1): p1.setType("P")
    return p1


def GetBarroLeeTerInCompleted(lang, female=False):
    en = ""
    sp = ""
    if female:
        en = "Female"
        sp = "femenina"

    p1 = Plot( Text("Share","Porcentaje") , Text(en + " Population with (in)completed tertiary","Poblacion " +sp + "con educacion terciaria (in)completa"), Text("Share","Porcentaje")) 
    tot = AddBarroLeeDataToPlotDecades(p1, lang, "TER.ICMP", female)
    if (tot <= 1): p1.setType("P")
    return p1


def GetTertiaryCompletionPlots(lang):
    plots= []
    plots.append(GetBarroLeeTerCompleted(lang).getPlotDict(lang))
    plots.append(GetBarroLeeTerCompleted(lang, True).getPlotDict(lang))
    return plots

def GetTertiaryInCompletionPlots(lang):
    plots= []
    plots.append(GetBarroLeeTerInCompleted(lang).getPlotDict(lang))
    plots.append(GetBarroLeeTerInCompleted(lang, True).getPlotDict(lang))
    return plots
