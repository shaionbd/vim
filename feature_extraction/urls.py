from . import views
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
	
	url(r'^$', views.index, name="featureExtractionIndex"),
	url(r'^features-extraction/', views.getFeature, name="featureExtractionUpload"),
	url(r'^features-extraction-process/', views.process, name="featuresExtractionProcess"),
    url(r'^associate-rule/', views.associateRule, name="associateRule"),

]
