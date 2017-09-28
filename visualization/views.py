# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render

import os, glob, time
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# Create your views here.

BASE_VIEW = "visualization/templates/"

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
        "is_active": "visualization",
        "is_visualize": False,
        "chart": False
    }
    
    return render(request, page, content)

def getGraphVisualization(request):

    BASE = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(BASE + "/templates/upload_files/demo.csv")

    input = request.POST['feature']  # receive the post request
    column = df[input]

    if np.issubdtype(column.dtype, np.number):

        directory = BASE + "/templates/upload_files/"
        os.chdir(directory)
        filelist = glob.glob("*.png")
        for file in filelist:
            os.remove(file)

        ts = int(time.time())
        img = str(ts)+".png"
        temp = sorted(column)
        pdf = stats.norm.pdf(temp, np.mean(temp), np.std(temp))
        plt.hist(temp, normed=True, facecolor='green', alpha=0.75)    # use this to draw histogram of your data
        plt.xlabel(input)
        plt.ylabel('frequency')
        plt.savefig(BASE + "/templates/upload_files/"+img)

    else:

        directory = BASE + "/templates/upload_files/"
        os.chdir(directory)
        filelist = glob.glob("*.png")
        for file in filelist:
            os.remove(file)
            
        ts = int(time.time())
        img = str(ts)+".png"
        column.value_counts().plot(kind='bar', facecolor='red', alpha=0.75)
        plt.xlabel(input)
        plt.ylabel('frequency')
        plt.savefig(BASE + "/templates/upload_files/"+img)

    image = "/static/visualization/templates/upload_files/"+img

    return HttpResponse(image)
    