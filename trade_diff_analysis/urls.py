from . import views
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [

    url(r'^$', views.index, name="tradeDiffIndex"),
    url(r'^select-year/', views.getFeature, name="selectYear"),
    url(r'^trade-diff-graph-visualization/', views.getGraphVisualization, name="tradeDiffGraphVisualization"),

]
