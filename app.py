from flask import Flask
import numpy as np
import random
import folium
from folium.plugins import MarkerCluster
from IPython.display import display
import webbrowser
from flask_paginate import Pagination, get_page_args,get_page_parameter
import json
import pdb
from datetime import datetime
from flask import Flask,render_template, request,jsonify,url_for
import duckdb
import mysql.connector

app = Flask(__name__)

def statistiquesByGravite():
    query="SELECT gravite, count(*) as total FROM usagers group by gravite"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

#Total Usagers
def incidentByGravite():
    query="SELECT count(*) as total FROM usagers WHERE gravite='Tué'"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

#Liste des usagers impliqués
def allUsagers():
    query="SELECT count(*) as total FROM usagers"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

#Liste de tous les incidents
def allIncidents():
    query="SELECT count(*) as total FROM caracteristiques"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

#Incident par Commune
def incidentByCommune():
    query="SELECT count(DISTINCT(commune)) as total from caracteristiques"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

#Incident par département
def incidentByDepartement():
    query="SELECT count(DISTINCT(departement)) as total FROM caracteristiques"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

def statAccidentByMonth():
    query="SELECT month(date_accident) as month,mois,count(*) as total FROM caracteristiques group by month(date_accident) order by month(date_accident) ASC;"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

#Top 5 des régions impactées
def topFiveCommunes():
    query="SELECT commune,count(*) FROM `caracteristiques` group by commune order by count(*) DESC LIMIT 10;"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

def statIncidentBySexe():
    query="SELECT sexe,count(*) as total FROM `usagers` group by sexe"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

def listOfGravite():
    query="SELECT DISTINCT(sexe) as sexe FROM usagers"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

#Liste des mois par ordre décroissant. De Janvier à Décembre
def getMonths():
    query="SELECT distinct(mois) FROM caracteristiques order by month(date_accident) ASC"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

#Obtention de l'état de gravité des usagers
def getGraviteByMonth(month,sexe):
    query="SELECT mois,sexe,count(sexe) FROM usagers,caracteristiques WHERE caracteristiques.accident_id=usagers.accident_id and mois=%s and sexe=%s group by mois,sexe;"
    parameters=(month,sexe)
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query,parameters)
    return mycursor.fetchall()

def returnReplacedValue(value,searchContent,integerValue):
    return value.replace(searchContent,str(integerValue))

#Requête des conditions atmosphériques
def getConditionsAtmospheriques():
    query="SELECT conditions_atmospheriques,count(*) FROM caracteristiques group by conditions_atmospheriques;"
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()

def getStatConditionsByMonth(mois,condition):
    query="SELECT mois,conditions_atmospheriques,count(conditions_atmospheriques) as total FROM caracteristiques WHERE  mois=%s and conditions_atmospheriques=%s group by conditions_atmospheriques;"
    parameters=(mois,condition)
    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
    mycursor=mysqldb.cursor()
    mycursor.execute(query,parameters)
    return mycursor.fetchall()

#Méthode de génération des coleurs aléatoires
def generateRandomColors():
    secondValue=random.randint(0,255)
    middle=random.randint(0,255)
    result="rgba(0,"+str(secondValue)+","+str(middle)+",1)"
    return result

@app.route('/')
def hello():
    labelsConditionsLine=[]
    datasConditionsLine=[]
    labelsBar=[]
    monthsLabels=[]
    myData=[]
    myColor=""

    months=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
    for condition in getConditionsAtmospheriques():
        for m in months:
            res=getStatConditionsByMonth(m,condition[0])
            if len(res)==1:
                datasConditionsLine.append(res[0][2])
            else:
                datasConditionsLine.append(0)
        labelCond={
        'label':condition[0],
        'data':datasConditionsLine,
        'backgroundColor':generateRandomColors(),
        'fill':'true'
        }
        labelsConditionsLine.append(labelCond)
        datasConditionsLine=[]

    for m in getMonths():
        monthsLabels.append(m[0])

    for sexe in listOfGravite():
        myColor=generateRandomColors()
        for month in getMonths():
            result=getGraviteByMonth(month[0],sexe[0])
            myData.append(result[0][2])
        resultLabel={
        'label':sexe[0],
        'data':myData,
        'backgroundColor':myColor
        }
        labelsBar.append(resultLabel)
        myData=[]
    
    statLibelle=[]
    statTotal=[]

    #Donut Chart Variables
    dataDonuts=[]
    labelsDonut=[]

    #Top Five Commune variables
    labelsFiveValue=[]
    dataFiveValue=[]

    #Variable Line Chart
    labelsLineChart=[]
    valueDataLineChart=[]

    statGravite=statistiquesByGravite()
    for stat in statGravite:
        statLibelle.append(stat[0])
        statTotal.append(stat[1])

    totalIncident=allIncidents()[0]
    incidentDepartement=incidentByDepartement()[0]
    incidentCommune=incidentByCommune()[0]
    totalUsagers=allUsagers()[0]
    gravite=incidentByGravite()[0]

    statByMonth=statAccidentByMonth()
    for value in statByMonth:
        labelsLineChart.append(value[1])
        valueDataLineChart.append(value[2])

    statTopByCommunes=topFiveCommunes()
    for val in statTopByCommunes:
        labelsFiveValue.append(val[0])
        dataFiveValue.append(val[1])

    statBySexe=statIncidentBySexe()
    for stat in statBySexe:
        labelsDonut.append(stat[0])
        dataDonuts.append(stat[1])
    
    return render_template("index.html",months=json.dumps(months),lblCndLine=json.dumps(labelsConditionsLine),dataLabels=json.dumps(labelsBar),labelsMonthsBar=json.dumps(monthsLabels),dataDonuts=json.dumps(dataDonuts),labelsDonuts=json.dumps(labelsDonut),labelsFive=json.dumps(labelsFiveValue),dataFive=json.dumps(dataFiveValue),dataLine=json.dumps(valueDataLineChart),labelsLine=json.dumps(labelsLineChart),total=json.dumps(statTotal),libelle=json.dumps(statLibelle),gravite=gravite[0],usagers=totalUsagers[0],commune=incidentCommune[0],departement=incidentDepartement[0],totalIncident=totalIncident[0])