# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render

import os, glob, time
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Create your views here.

BASE_VIEW = "trade_diff_analysis/templates/"

def index(request):

    #enter your all logics
    page = BASE_VIEW + "views/pages/index.html"
    content = {

        "title": "VIM",
        
    }

    return render(request, page, content)


def getFeature(request):

    BASE = os.path.dirname(os.path.abspath(__file__))
    df_from_year = pd.read_csv(BASE + "/templates/trade_diff_files/" + request.POST["from_year"] + ".csv", encoding = "ISO-8859-1")
    df_to_year = pd.read_csv(BASE + "/templates/trade_diff_files/" + request.POST["to_year"] + ".csv", encoding = "ISO-8859-1")


    featureListFromYear = list(df_from_year)
    featureListToYear = list(df_to_year)
    feature_name_from_year = []
    feature_name_to_year = []
    
    for index, value in enumerate(featureListFromYear):
        feature_name_from_year.append(value)
    
    for index, value in enumerate(featureListToYear):
        feature_name_to_year.append(value)

    page = BASE_VIEW + "views/pages/features.html"
    content = {
        "title": "VIM",
        "from_year_features": feature_name_from_year,
        "to_year_features": feature_name_to_year,
        "from_year": request.POST["from_year"],
        "to_year": request.POST["to_year"],
    }

    return render(request, page, content)


def getGraphVisualization(request):

    # return HttpResponse(request.POST["feature"])

    BASE = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(BASE + "/templates/trade_diff_files/" + request.GET["year"] + ".csv", encoding = "ISO-8859-1")
    
    input = request.GET["feature"]  # receive the post request
    column = df[input]

    if np.issubdtype(column.dtype, np.number):

        ts = int(time.time())
        img = str(ts)+".png"
        temp = sorted(column)
        pdf = stats.norm.pdf(temp, np.mean(temp), np.std(temp))
        plt.hist(temp, normed=True, facecolor='green', alpha=0.75)  # use this to draw histogram of your data
        plt.xlabel(input)
        plt.ylabel('frequency')

        if request.GET["year_status"] == "from_year":

            directory = BASE + "/templates/from_year_graphs/"
            os.chdir(directory)
            filelist = glob.glob("*.png")
            for file in filelist:
                os.remove(file)

            plt.savefig(BASE + "/templates/from_year_graphs/"+img)

        else:

            directory = BASE + "/templates/to_year_graphs/"
            os.chdir(directory)
            filelist = glob.glob("*.png")
            for file in filelist:
                os.remove(file)

            plt.savefig(BASE + "/templates/to_year_graphs/"+img)            
    
    else:

        ts = int(time.time())
        img = str(ts)+".png"
        column.value_counts().plot(kind='bar', facecolor='red', alpha=0.75)
        plt.xlabel(input)
        plt.ylabel('frequency')

        if request.GET["year_status"] == "from_year":

            directory = BASE + "/templates/from_year_graphs/"
            os.chdir(directory)
            filelist = glob.glob("*.png")
            for file in filelist:
                os.remove(file)

            plt.savefig(BASE + "/templates/from_year_graphs/"+img)

        else:

            directory = BASE + "/templates/to_year_graphs/"
            os.chdir(directory)
            filelist = glob.glob("*.png")
            for file in filelist:
                os.remove(file)

            plt.savefig(BASE + "/templates/to_year_graphs/"+img)

    if request.GET["year_status"] == "from_year":
        image = "/static/trade_diff_analysis/templates/from_year_graphs/"+img
    else:
        image = "/static/trade_diff_analysis/templates/to_year_graphs/"+img

    return HttpResponse(image)

