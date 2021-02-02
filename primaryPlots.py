from .viewHelper import *


PrimaryPlots = [{"name":"completed","en_name":"Completed Primary","sp_name":"Primaria Completa","pk":1},
                {"name":"incompleted","en_name":"Completed and Incompleted Primary","sp_name":"Primaria Completa e Incompleta","pk":2},
                {"name":"grad","en_name":"Gross Graduation Ratio","sp_name":"Tasa bruta de graduacion","pk":3}]


###################################################################################
# Primary Schooling
#
#

def GetBarroLeePrimCompleted(lang, female=False):
    en = ""
    sp = ""
    if female:
        en = "Female"
        sp = "femenina"

    p1 = Plot( Text("Share","Porcentaje") , Text(en + " Population with completed primary","Poblacion " +sp + "con escuela primaria completa"), Text("Share","Porcentaje")) 
    tot = AddBarroLeeDataToPlotDecades(p1, lang, "PRM.CMPT", female)
    if (tot == 1): p1.setType("P")
    return p1


def GetBarroLeePrimInCompleted(lang, female=False):
    en = ""
    sp = ""
    if female:
        en = "Female"
        sp = "femenina"

    p1 = Plot( Text("Share","Porcentaje") , Text(en + " Population with (in)completed primary","Poblacion " +sp + "con escuela primaria (in)completa"), Text("Share","Porcentaje")) 
    tot = AddBarroLeeDataToPlotDecades(p1, lang, "PRM.ICMP", female)
    if (tot <= 3): p1.setType("P")
    return p1


def GetPrimaryCompletionPlots(lang):
    plots= []
    plots.append(GetBarroLeePrimCompleted(lang).getPlotDict(lang))
    plots.append(GetBarroLeePrimCompleted(lang, True).getPlotDict(lang))
    return plots

def GetPrimaryInCompletionPlots(lang):
    plots= []
    plots.append(GetBarroLeePrimInCompleted(lang).getPlotDict(lang))
    plots.append(GetBarroLeePrimInCompleted(lang, True).getPlotDict(lang))
    return plots



def GetPrimaryGraduationRatio(lang):
    p1 = Plot( Text("Porcentual","Porcentaje") , Text("Graduation Ratio","Tasa de Graduacion"), Text("Porcentual","Porcentaje"))
    
    indicators_en_def = {"SE.PRM.CMPL.FE.ZS":"female","SE.PRM.CMPL.MA.ZS":"male","SE.PRM.CMPL.ZS":"both sexes"}
    indicators_sp_def = {"SE.PRM.CMPL.FE.ZS":"femenino","SE.PRM.CMPL.MA.ZS":"masculino","SE.PRM.CMPL.ZS":"ambos"}
    
    plot_indicators = ["SE.PRM.CMPL.FE.ZS", "SE.PRM.CMPL.MA.ZS","SE.PRM.CMPL.ZS"]
    
    tot = AddDataToPlot(p1, lang, indicators_en_def, indicators_sp_def, plot_indicators)
    if (tot <= 3): p1.setType("P")

    return p1



def GetPrimaryOutOfSchoolRatio(lang):
    p1 = Plot( Text("Porcentual","Porcentaje") , Text("Out-of-school Children","Niños no escolarizados"), Text("Porcentual","Porcentaje"))
    
    indicators_en_def = {"SE.PRM.UNER.FE.ZS":"female","SE.PRM.UNER.MA.ZS":"male","SE.PRM.UNER.ZS":"both sexes"}
    indicators_sp_def = {"SE.PRM.UNER.FE.ZS":"femenino","SE.PRM.UNER.MA.ZS":"masculino","SE.PRM.UNER.ZS":"ambos"}
    
    plot_indicators = ["SE.PRM.UNER.FE.ZS", "SE.PRM.UNER.MA.ZS","SE.PRM.UNER.ZS"]
    
    tot = AddDataToPlot(p1, lang, indicators_en_def, indicators_sp_def, plot_indicators)
    if (tot <= 3): p1.setType("P")

    return p1

def GetPrimaryGradPlots(lang):
    plots= []

    plots.append(GetPrimaryGraduationRatio(lang).getPlotDict(lang))
    plots.append(GetPrimaryOutOfSchoolRatio(lang).getPlotDict(lang))

    return plots


