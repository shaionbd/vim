from . import views
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [

    url(r'^$', views.index, name="visualizationIndex"),
    url(r'^visualization-features-extraction/', views.getFeature, name="visualizationUpload"),
    url(r'^graph-visualization/', views.getGraphVisualization, name="graphVisualization"),
    
]
