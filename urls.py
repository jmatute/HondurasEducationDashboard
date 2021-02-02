from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='dashboard'),
    url(r'geojson/$',views.geojson, name='geojson'),
    url(r'mapData/$',views.getMapIndicatorData, name='getMapIndicator'),
    url(r'indicators/$', views.getIndicators, name='allIndicators'),
    url(r'progressData/$',views.getProgressIndicatorData, name='getProgressIndicator'),
    url(r'generalAccess/$',views.getGenAccessData, name='getGeneralAccessPlot'),
    url(r'primary/$',views.getPrimarySchoolingData, name='getPrimarySchoolingPlot'),
    url(r'secondary/$',views.getSecondarySchoolingData, name='getSecondarySchoolingPlot'),
    url(r'tertiary/$',views.getTertiarySchoolingData, name='getTertiarySchoolingPlot'),

]


