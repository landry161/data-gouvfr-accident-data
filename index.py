import pdb
import pandas as pd
import csv
import os
import geopandas as gpd
from flask import Flask,render_template, request,jsonify,url_for
import mysql.connector

monthDictionnary={1:"Janvier",2:"Février",3:"Mars",4:"Avril",5:"Mai",6:"Juin",7:"Juillet",8:"Août",9:"Septembre",10:"Octobre",11:"Novembre",12:"Décembre"}
localisationDictionnary={1:"Hors agglomération",2:"En agglomération"}
collisionDictionnary={-1:"Non renseigné",1:"Deux véhicules - frontale",2:"Deux véhicules – par l’arrière",3:"Deux véhicules – par le coté",4:"Trois véhicules et plus – en chaîne",5:"Trois véhicules et plus - collisions multiples",6:"Autre collision",7:"Sans collision"}
intersectionDictionnary={1:"Hors intersection",2:"Intersection en X",3:"Intersection en T",4:"Intersection en Y",5:"Intersection à plus de 4 branches",6:"Giratoire",7:"Place",8:"Passage à niveau",9:"Autre intersection"}
conditionsAtmospheriquesDictionnary={-1:"Non renseigné",1:"Normale",2:"Pluie légère",3:"Pluie forte",4:"Neige - grêle",5:"Brouillard - fumée",6:"Vent fort - tempête",7:"Temps éblouissant",8:"Temps couvert",9:"Autre"}
conditions={1:"Plein jour",2:"Crépuscule ou aube",3:"Nuit sans éclairage public",4:"Nuit avec éclairage public non allumé",5:"Nuit avec éclairage public allumé"}

def getDepartementByNumber(depNumber):
	departement=pd.read_csv("departement_2022.csv",delimiter='\t')
	valueDep=""
	for dep in departement.values:
		values=dep[0].split(",")
		if depNumber==(values[0]):
			valueDep=values[4]
	return valueDep

def getCommuneByCode(code):
	communes=pd.read_csv("commune_2022.csv",delimiter="\t")
	valueCommune=""
	for com in communes.values:
		commune=com[0].split(",")
		if code==commune[1]:
			valueCommune=commune[7]
	return valueCommune

def createCaracteristiqueFinalFile():
	print("Génération en cours...")
	file=open("caracteritiques_final.csv","w")
	file.write('accident_id;date_accident;heure;conditions;departement;commune;localisation;intersection;conditions_atmospheriques;collision;adresse;lat;lng;mois\n')
	myPandasFile=pd.read_csv("carcteristiques-2022.csv",delimiter='\t')
	arrayValues=myPandasFile.values

	for val in range(0,len(arrayValues)):
		print(val,"Ligne(s) écrites ")
		element=arrayValues[val][0].split(";")
		accident_id=element[0].replace('"',"")
		
		day=int(element[1].replace('"',""))
		month=int(element[2].replace('"',""))
		year=int(element[3].replace('"',""))
		libelleAdresse=element[12].replace('"',"")

		libelleLat=(element[13].replace('"',"").replace('"',"")).replace(",",".")
		libelleLng=(element[14].replace('"',"").replace('"',"")).replace(",",".")
		libelleHeure=element[4].replace('"',"")
		libelleMois=monthDictionnary[int(month)]
		libelleLocalisation=localisationDictionnary[int(element[8].replace('"',""))]
		libelleDate=str(day)+"-"+str(month)+"-"+str(year)
		libelleCollision=collisionDictionnary[int(element[11].replace('"',""))]
		libelleIntersection="Non renseigné" if int(element[9].replace('"',""))==-1 else intersectionDictionnary[int(element[9].replace('"',""))]
		
		libelleConditionsAtmospheriques=conditionsAtmospheriquesDictionnary[int(element[10].replace('"',""))]
		libelleCommune=getCommuneByCode(element[7].replace('"',''))
		libelleConditions=collisionDictionnary[int(element[5].replace('"',""))]
		
		if element[6].replace('"','')=="2A":
			libelleDepartement="Corse du Sud"
		elif element[6].replace('"','')=="2B":
			libelleDepartement="Haute Corse"
		else:
			libelleDepartement=getDepartementByNumber(element[6].replace('"',''))
		file.write(str(accident_id)+";"+str(libelleDate)+";"+str(libelleHeure)+";"+str(libelleConditions)+";"+str(libelleDepartement)+";"+str(libelleCommune)+";"+str(libelleLocalisation)+";"+str(libelleIntersection)+";"+str(libelleConditionsAtmospheriques)+";"+str(libelleCollision)+";"+str(libelleAdresse)+";"+str(libelleLat)+";"+str(libelleLng)+";"+str(libelleMois)+"\n")
	file.close()

def insertIntoDB(accident_id,libelleDate,libelleHeure,libelleConditions,libelleDepartement,libelleCommune,libelleLocalisation,libelleIntersection,libelleConditionsAtmospheriques,libelleCollision,libelleAdresse,libelleLat,libelleLng,libelleMois):
	mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="accidentapp")  
	mycursor=mysqldb.cursor()
	try:
		query="INSERT INTO caracteristiques(accident_id,date_accident,heure,conditions,departement,commune,localisation,intersection,conditions_atmospheriques,collision,adresse,lat,lng,mois) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		parameters=(accident_id,libelleDate,libelleHeure,libelleConditions,libelleDepartement,libelleCommune,libelleLocalisation,libelleIntersection,libelleConditionsAtmospheriques,libelleCollision,libelleAdresse,libelleLat,libelleLng,libelleMois)
		mycursor.execute(query,parameters)
		print("Ajout de ",str(accident_id)," ...")
		mysqldb.commit()
	except NameError:
		print(NameError)
		mysqldb.rollback()

def fetchCSVFile():
	rows=pd.read_csv("caracteritiques_final.csv",encoding="ISO-8859-1",delimiter='\t')
	for file in range(0,len(rows.values)):
		element=rows.values[file][0].split(";")
		dateElement=element[1].split("-")
		year=dateElement[2]
		month=dateElement[1]
		day=dateElement[0]

		dateLibelle=str(year)+"-"+str(month)+"-"+str(day)
		insertIntoDB(element[0],element[1],element[2],element[3],element[4],element[5],element[6],element[7],element[8],element[9],element[10],element[11],element[12],element[13])

#Appel de la fonction
createCaracteristiqueFinalFile()
fetchCSVFile()