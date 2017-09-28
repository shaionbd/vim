from django.http import HttpResponse
from django.shortcuts import render

import os
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
# import weka.core.jvm as jvm
# import weka.core.converters as converters
# from weka.associations import Associator

# Create your views here.

BASE_VIEW = "feature_extraction/templates/"

def index(request):

    page = BASE_VIEW + "views/pages/index.html"
    content = { 
        "title": "VIM"
    }

    return render(request, page, content)

def getFeature(request):

    upload_file = request.FILES["csv_file"]
    df = pd.read_csv(upload_file)

    BASE = os.path.dirname(os.path.abspath(__file__))
    df.to_csv(BASE + "/templates/upload_files/demo.csv", index=False)

    featureList = list(df)
    feature_name = []
    
    for index, value in enumerate(featureList):
        feature_name.append(value)

    page = BASE_VIEW + "views/pages/features.html"
    content = {
        "title": "VIM", 
        "features": feature_name,
        "is_process": False,
        "is_visualize": False,
        "chart": False
    }
    
    return render(request, page, content)

def process(request):

    # if this is a POST request we need to process the form data
    if (request.method == 'POST'):

        # get url from input
        dataList = request.POST.getlist('features[]')

        BASE = os.path.dirname(os.path.abspath(__file__))
        df = pd.read_csv(BASE+"/templates/upload_files/demo.csv")

        test = {}
        feature_name = []
        featureList = list(df)

        for data in dataList:
            test[data] = df[data]

        for index, value in enumerate(featureList):
            feature_name.append(value)

        new_df = pd.DataFrame(test)
        new_df.to_csv(BASE+"/templates/upload_files/export.csv", index=False)

        new_df = pd.read_csv(BASE + "/templates/upload_files/export.csv")

        new_df.to_html(BASE + "/templates/views/table.html", index= False)

        page = BASE_VIEW + "views/pages/features.html"
        content = {
            "title": "VIM",
            "features": feature_name,
            "export_url": BASE_VIEW+"/upload_files/export.csv",
            "is_process": True,
            "is_visualize": False,
            "chart": False
        }

        return render(request, page, content)

def associateRule(request):
    
    jvm.start()
    
    data_dir = os.path.dirname(os.path.abspath(__file__))
    data = converters.load_any_file(data_dir + "/templates/upload_files/export.csv")
    data.class_is_last()
    
    associator = Associator(classname="weka.associations.Apriori", options=["-C", "-1", "-I"])
    # associator = Associator(classname="weka.associations.Apriori", options=["-N", "9", "-I"])
    associator.build_associations(data)

    rules = str(associator)
    
    jvm.stop()
    
    return HttpResponse(rules)
