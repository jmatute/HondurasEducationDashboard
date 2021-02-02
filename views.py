from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

import json
import os
from django.apps import apps
from .models import *
from .viewHelper import *
from .primaryPlots import *
from .secondaryPlots import *
from .tertiaryPlots import *

def index(request):

    mapIndicators    = BooleanMapIndicator.objects.all().values('indicator').distinct()
    indicatorsId     = [e[0] for e in mapIndicators.values_list('indicator')]
    mapIndicatorList = Indicator.objects.filter(pk__in=indicatorsId)
    
    assistanceIndicator = Indicator.objects.get(name="Asistencia.escolar")
    currentMapSelection = BooleanMapIndicator.objects.filter(indicator=assistanceIndicator) 
    numAnswer = currentMapSelection.values('answer').distinct().count() #
    
    options = []
    total_options = 0

    map_data = getPerDepartmentMapData(assistanceIndicator,"Si")
    progressIndicatorsId = ProgressIndicator.objects.values_list('indicator').distinct()
    progressIndicatorList = Indicator.objects.filter(pk__in=list(map(lambda x:x[0],progressIndicatorsId)))

    progress_values = getProgressIndicatorInfo("Education Index")
    
    options = [e for e in currentMapSelection.values_list('answer','eng_answer').distinct()]     
    total_options = len(options)
    
    withIndex = []
    for i in range(len(options)):
        withIndex.append({"index":i,"answer":options[i][0], "eng_answer":options[i][1] })


    context = {"indicators":mapIndicatorList, 'options':withIndex,'total_options':total_options,
               "map_data":map_data, "progress_val":progress_values, "progress_index_name":"Education Index",
               "progress_indicators":progressIndicatorList, "genAccess": GenAccessPlots }

    context['primarySchooling']   = PrimaryPlots
    context['secondarySchooling'] = SecondaryPlots
    context['tertiarySchooling']  = TertiaryPlots


    return render(request,'dashboard/index.html', context)

def geojson(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR = os.path.join(BASE_DIR, 'public_html/static/data')
    geojson_path = os.path.join(BASE_DIR,'simplerAdmin1.geojson')
    response_data = {}
    with open(geojson_path) as json_file:
        response_data = json.load(json_file)

    return HttpResponse(json.dumps(response_data),content_type="application/json")



def getMapIndicatorData(request):
    #need only answer and indicator
    #and the options 
    response_data = {}
    
    indicatorId = request.GET.get('mapIndicator','')
    answer = request.GET.get('answer','')
    language = request.GET.get('lang','en')

    wantedIndicator = Indicator.objects.get(pk=indicatorId)

    currentMapSelection = BooleanMapIndicator.objects.filter(indicator=wantedIndicator)
    answerList = [e for e in currentMapSelection.values_list('answer','eng_answer').distinct() ]
   
    eng_answer = ""
    if answer not in list(map(lambda x:x[0],answerList)):
        answer = answerList[0][0]
        eng_answer = answerList[0][1]
    else:
        for elem in answerList:
            if elem[0] == answer:
                eng_answer = elem[1]
                break

    response_data = getPerDepartmentMapData(wantedIndicator, answer)
    
    withIndex = []
    for i in range(len(answerList)):
        withIndex.append({"index":i,"answer":answerList[i][0],"eng_answer":answerList[i][1] })

    response_data['new_options'] = withIndex

    answerIndex = 0
    if language == "en":
        answerIndex = 1
        answer = eng_answer

    response_data['current_answer'] = answer
    response_data['total_options'] = len(answerList)
    return HttpResponse(json.dumps(response_data),content_type="application/json")



def getProgressIndicatorData(request):
    response_data = {}
    indicatorId = request.GET.get('Indicator','')
    language = request.GET.get('lang','en')
    
    wantedIndicator = Indicator.objects.get(pk=indicatorId)
    progress_values = getProgressIndicatorInfo(wantedIndicator.en_name)
    response_data["progress_val"] = progress_values
    
    response_data["progress_index_name"] = wantedIndicator.en_name
    if language == "sp":
        response_data["progress_index_name"] = wantedIndicator.sp_name

    return HttpResponse(json.dumps(response_data),content_type="application/json")



def getGenAccessData(request):
    response_data = {}
    language = request.GET.get('lang','en')
    genAccessName = request.GET.get('name','')

    if genAccessName == "literacy":
        response_data = GetLiteracyRatePlotData(language)
    if genAccessName == "access":
        response_data =  GetOverallAccessPlots(language)
    if genAccessName == "noed":
        response_data =  GetNoEducationPlots(language)

    return HttpResponse(json.dumps(response_data),content_type="application/json")


def getPrimarySchoolingData(request):
    response_data = {}
    language = request.GET.get('lang','en')
    primaryName = request.GET.get('name','')

    if primaryName == "completed":
        response_data = GetPrimaryCompletionPlots(language)
    if primaryName == "incompleted":
        response_data = GetPrimaryInCompletionPlots(language)
    if primaryName == "grad":
        response_data = GetPrimaryGradPlots(language)

    return HttpResponse(json.dumps(response_data),content_type="application/json")


def getSecondarySchoolingData(request):
    response_data = {}
    language = request.GET.get('lang','en')
    secondaryName = request.GET.get('name','')

    if secondaryName == "completed":
        response_data = GetSecondaryCompletionPlots(language)
    if secondaryName == "incompleted":
        response_data = GetSecondaryInCompletionPlots(language)

    return HttpResponse(json.dumps(response_data),content_type="application/json")


def getTertiarySchoolingData(request):
    response_data = {}
    language = request.GET.get('lang','en')
    tertiaryName = request.GET.get('name','')

    if tertiaryName == "completed":
        response_data = GetTertiaryCompletionPlots(language)
    if tertiaryName == "incompleted":
        response_data = GetTertiaryInCompletionPlots(language)

    return HttpResponse(json.dumps(response_data),content_type="application/json")


def getIndicators(request):
    context = {}
    all_indicators = []
    
    access        =  AccessIndicatorsNames()
    mapIndicators =  getMapIndicators()
    progress      =  getProgressIndicators()
   
   
    all_indicators.extend(access)
    all_indicators.extend(mapIndicators)
    all_indicators.extend(progress)

    all_indicators.extend(PrimarySchoolingIndicatorsNames())
    all_indicators.extend(SecondarySchoolingIndicatorsNames())
    all_indicators.extend(TertiarySchoolingIndicatorsNames())

    all_indicators.sort()

    context["indicators"] = enumerate(Indicator.objects.filter(name__in=all_indicators))
    data_dict = {"context":context}
    return render(request,'dashboard/indicators.html', data_dict)
