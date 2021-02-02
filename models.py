from django.db import models

from memoize import memoize, delete_memoized, delete_memoized_verhash
from django.apps import apps
import os


class Indicator(models.Model):
    name               = models.CharField(max_length=100) 
    en_name            = models.CharField(max_length=100)
    sp_name            = models.CharField(max_length=100)
    en_description     = models.CharField(max_length=500)
    sp_description     = models.CharField(max_length=500)
    source             = models.CharField(max_length=200, default='')
    inner_destination  = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def getSpanishInfo(self):
        return self.sp_description

    def getEnglishInfo(self):
        return self.en_description

    def getDataSource(self):
        return self.source


    def defaultDefinedType(self):
        loweredDescription = self.en_description.lower()
        wordCombo = [("expenditure","I"), ("primary","P"), ("secondary","S"),("tertiary","T")]

        for combo in wordCombo:
            if combo[0] in loweredDescription:
                return combo[1]
        return "G"


class BooleanMapIndicator(models.Model):
    indicator       = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    year            = models.IntegerField()
    department_name = models.CharField(max_length=100,default='')
    num_cases       = models.IntegerField()
    porcentual      = models.DecimalField(max_digits=10,decimal_places=5)
    eng_name        = models.CharField(max_length=100, default='')
    answer          = models.CharField(max_length=100, default='')
    eng_answer      = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.indicator.name + ": sp: "+  str(self.answer) + " , eng : " + str(self.eng_answer) + "."

class SchoolingIndicator(models.Model):
    indicator          = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    indicator_options  = [ ('P','Primary'),('S','Secondary'),('T','Tertiary'), ('I','Investment'), 
                           ('G','General')]
    type_schooling     = models.CharField(max_length=2, choices=indicator_options, blank=False)
    year               = models.IntegerField()
    value              = models.DecimalField(max_digits=20,decimal_places=10)
    
    def __str__(self):
        return self.indicator.name + ":"+  str(self.year) + " , " + str(self.value)

class ProgressIndicator(models.Model):
    indicator         = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    region_options    = [ ('C','Country'),('R','Region'),('D','Development Stage')]
    region_type       = models.CharField(max_length=2, choices=region_options, blank=False)
    year              = models.IntegerField()
    current_ranking   = models.IntegerField(default=-1)
    region_name       = models.CharField(max_length=150)
    value              = models.DecimalField(max_digits=20,decimal_places=10)

