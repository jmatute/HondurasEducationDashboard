from .models import *
from django.db.models import Sum


GenAccessPlots = [{"name":"literacy","en_name":"Literacy","sp_name":"Alfabetismo","pk":1},
                  {"name":"access", "en_name":"Overall Access","sp_name":"Acceso General","pk":2},
                  {"name":"noed", "en_name":"No Education","sp_name":"Sin Educación","pk":3}]


class Text():

    def __init__(self, en_value, sp_value):
        self.en = en_value
        self.sp = sp_value

    def get(self, lang):
        if lang == "en":
            return self.en
        else:
            return self.sp


class Plot():
    #title plot, subtitle, yAxis, grouping_variable, value

    def __init__(self, title, subtitle, yAxisName):
        
        self._title = title
        self._subtitle = subtitle
        self._yAxis = yAxisName
        self.items = []
        self.type = "L"
    
    def addItem(self, year, value, grouping_variable):
        self.items.append({"n":float(value), "year":year, "type":grouping_variable})
        

    def getType(self):
        return self.type

    def setType(self, value):
        self.type = value

    def getPlotDict(self, lang):

        return {"title":self._title.get(lang),
                "subtitle":self._subtitle.get(lang),
                "yaxis":self._yAxis.get(lang),
                "items":self.items,
                "type":self.getType()}




def getPerDepartmentMapData(indicator, answer):

    currentMapSelection = BooleanMapIndicator.objects.filter(indicator=indicator)
    popPerDept = currentMapSelection.values('department_name').annotate(Sum('num_cases'))

    map_data = {}
    for dpt in popPerDept:
        name = dpt['department_name']
        total_cases = dpt['num_cases__sum']
        sampleDpt = currentMapSelection.filter(department_name=name).get(answer=answer)
        incidence = sampleDpt.num_cases/float(total_cases) # force floating point arithmetic
        map_data[name] = {'total_dept':total_cases,'total_answer':float(sampleDpt.num_cases),
                'porcentual':float(sampleDpt.porcentual),'per1000': incidence*1000.0}
    return map_data


def getProgressIndicatorInfo(name_indicator):
    educationIndicesValues = ProgressIndicator.objects.filter(indicator__en_name=name_indicator)
    #educationIndicesValues = educationIndicesValues.filter(region_type="C")
    progress_data = []
    #Per region_name extract the values
    regions = [e[0] for e in educationIndicesValues.values_list('region_name').distinct()]
    
    for region in regions:
        regionValues   = educationIndicesValues.filter(region_name=region).order_by('year')
        for perYear in regionValues:
            progress_data.append({'region':region,'type':perYear.region_type, 
                                  'year':perYear.year,'n':float(perYear.value)})

    return progress_data



#### Plot Definitions  #####
#
#   Description of all plots to be used and grouped.
#   Per plot it should contain (minimum) >  
#        title plot, subtitle, yAxis, grouping_variable, value
#
#
############################
#     General Access:
# 

def AddDataToPlot(plot, lang, en_dict, sp_dict,plot_indicators, multiplier = 1.0):
   
    total_years = set([])
    for indicator in plot_indicators:
        name = en_dict[indicator]
        if lang == "sp":
            name = sp_dict[indicator]
        currentIndicatorValues = SchoolingIndicator.objects.filter(indicator__name=indicator).order_by('year')

        for elem in currentIndicatorValues:
            plot.addItem(elem.year, float(elem.value)* multiplier, name) 
            total_years.add(elem.year)
    return len(total_years)


def AddBarroLeeDataToPlotDecades(plot, lang, indicator, female= False):
    total_years = set([])

    #joined by decades
    decades = {  "15-19":["1519"],"20-29":["2024","2529"] ,"30-39":["3034","3539"], "40-49": ["4044","4549"], "50-59":["5054","5559"] ,"60-64":["6064"] }
    totalsAllPerYear = {}

    for key, value in decades.items():

        name = key
        totalsPerYear = {}

        for sub in value:
            popIndicatorName = "BAR.POP." + sub
            valueIndicatorName = "BAR."+ indicator + "." + sub
            
            if female:
                valueIndicatorName += ".FE.ZS"
                popIndicatorName += ".FE"
            else:
                valueIndicatorName += ".ZS"

            populationIndicatorValues = SchoolingIndicator.objects.filter(indicator__name=popIndicatorName).order_by('year')
            percentIndicatorValues    = SchoolingIndicator.objects.filter(indicator__name=valueIndicatorName).order_by('year')
           
            
            for elem in percentIndicatorValues:
                #TODO-this works in case of duplication in dataset...
                curYearPopulation = populationIndicatorValues.filter(year=elem.year).values('value','year').distinct()
                curYearPopulation = curYearPopulation[0] 
                
                totalInThousands = (float(elem.value)/100.0 )*(float(curYearPopulation['value']))
                totalPop = (float(curYearPopulation['value']))
                if elem.year in totalsPerYear:
                    totalsPerYear[elem.year][0] += totalPop
                    totalsPerYear[elem.year][1] += totalInThousands
                else:
                    totalsPerYear[elem.year] = [totalPop, totalInThousands]

                if elem.year in totalsAllPerYear:
                    totalsAllPerYear[elem.year][0] += totalPop
                    totalsAllPerYear[elem.year][1] += totalInThousands
                else:
                    totalsAllPerYear[elem.year] = [totalPop, totalInThousands]


            
        for year, values in totalsPerYear.items():

            plot.addItem(year, ( values[1]/values[0] )*100, name) 
            total_years.add(year)

    for year, values in totalsAllPerYear.items():
        plot.addItem(year, ( values[1]/values[0] )*100, "Total") 
        total_years.add(year)


    return len(total_years)


#############################################################
#

def GetLiteracyRatePlotData(lang):
    plots = []
    
    indicators_en_def = {"SE.ADT.1524.LT.FE.ZS":"female (15-24)", "SE.ADT.1524.LT.MA.ZS":"male (15-24)",
                         "SE.ADT.LITR.FE.ZS": "female (15+)", "SE.ADT.LITR.MA.ZS": "male (15+)",
                         "SE.LPV.PRIM.FE": "female", "SE.LPV.PRIM.MA":"male"}

    indicators_sp_def = {"SE.ADT.1524.LT.FE.ZS":"femenino (15-24)", "SE.ADT.1524.LT.MA.ZS":"masculino (15-24)",
                         "SE.ADT.LITR.FE.ZS": "femenino (15+)", "SE.ADT.LITR.MA.ZS": "masculino (15+)",
                         "SE.LPV.PRIM.FE": "femenino", "SE.LPV.PRIM.MA":"masculino"}

    plot_indicators = ["SE.ADT.1524.LT.FE.ZS", "SE.ADT.1524.LT.MA.ZS", "SE.ADT.LITR.FE.ZS","SE.ADT.LITR.MA.ZS"]


    p1 = Plot( Text("Literacy Rate","Tasa de alfabetismo") , Text("age divided","rango de edad"), Text("Rate","Porcentaje"))
    tot = AddDataToPlot(p1, lang, indicators_en_def, indicators_sp_def, plot_indicators)
    if (tot <=3 ): p1.setType("P")
    plots.append(p1.getPlotDict(lang))

    # It only has one year.....TODO create a pie chart
    #plot_indicators = ["SE.LPV.PRIM.FE", "SE.LPV.PRIM.MA"]
    #p2 = Plot( Text("Learning Poverty","Pobreza de Aprendizaje") , Text("children below minimum reading proficiency","por debajo de la capacidad mínima de lectura"), Text("Rate","Porcentaje"))
    #tot = AddDataToPlot(p2, lang, indicators_en_def, indicators_sp_def, plot_indicators)
    #if (tot == 1): p2.setType("P")
    #plots.append(p2.getPlotDict(lang))
    return plots

##############################
#


def GetSchoolLifeExpectancy(lang):
    p1 = Plot( Text("School Life Expectancy","Esperanza de vida Escolar") , Text("Primary to tertiary","Primaria a terciaria"), Text("Years","Años"))
    
    indicators_en_def = {"SE.SCH.LIFE.FE":"female","SE.SCH.LIFE.MA":"male","SE.COM.DURS":"compulsory"}
    indicators_sp_def = {"SE.SCH.LIFE.FE":"femenino","SE.SCH.LIFE.MA":"masculino","SE.COM.DURS":"obligatorio"}

    plot_indicators = ["SE.SCH.LIFE.FE", "SE.SCH.LIFE.MA","SE.COM.DURS"]
    
    tot = AddDataToPlot(p1, lang, indicators_en_def, indicators_sp_def, plot_indicators)
    if (tot <=3  ): p1.setType("P")
    return p1

def GetYouthInSchool(lang):
    
    p1 = Plot( Text("Share","Porcentaje") , Text("Youth in School (15-24)","Juventud: En Escuela (15-24)"), Text("Share","Porcentaje"))
    
    indicators_en_def = {"4.0.stud.15a24":"In School","4.0.nini.15a24":"Neither in School nor working", "4.0.studwork.15a24":"In School and Employed",
                         "4.0.work.15a24":"Employed"}
    indicators_sp_def = {"4.0.stud.15a24":"Escuela","4.0.nini.15a24":"Ni trabajando ni escuela", "4.0.studwork.15a24":"Trabajando y estudiando",
                         "4.0.work.15a24":"Trabajando"}

    plot_indicators = ["4.0.stud.15a24", "4.0.nini.15a24","4.0.studwork.15a24","4.0.work.15a24"]

    tot = AddDataToPlot(p1, lang, indicators_en_def, indicators_sp_def, plot_indicators, 100.0)
    if (tot == 1): p1.setType("P")
    return p1


def GetOverallAccessPlots(lang):
    plots= []
    plots.append(GetSchoolLifeExpectancy(lang).getPlotDict(lang))
    plots.append(GetYouthInSchool(lang).getPlotDict(lang))
    return plots

##############################################################################


def GetBarroLeeNoEducation(lang):
    p1 = Plot( Text("Share","Porcentaje") , Text("Population with no Education","Poblacion sin Educacion"), Text("Share","Porcentaje"))
    tot = AddBarroLeeDataToPlotDecades(p1, lang, "NOED")
    if (tot <=3): p1.setType("P")
    return p1


def GetBarroLeeNoEducationFemale(lang):
    p1 = Plot( Text("Share","Porcentaje") , Text("Female Population with no Education","Poblacion femenina sin Educacion"), Text("Share","Porcentaje"))
    tot = AddBarroLeeDataToPlotDecades(p1, lang, "NOED",True)
    if (tot <= 3): p1.setType("P")
    return p1


def GetNoEducationPlots(lang):
    plots= []
    plots.append(GetBarroLeeNoEducation(lang).getPlotDict(lang))
    plots.append(GetBarroLeeNoEducationFemale(lang).getPlotDict(lang))

    return plots


