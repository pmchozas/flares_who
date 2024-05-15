#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 17:13:47 2024

@author: pmchozas
"""

import json
import spacy
import requests
import os
import csv

nlp = spacy.load('es_core_news_lg')

train_file= "5w1h_subtarea_1_train.json" #Path to dataset

testing_file="testing.json"
train_data=[]
with open(testing_file, "r") as f:
  for line in f.readlines():
      train_data.append(json.loads(line))
      
      


# Ruta de la carpeta que contiene los archivos CSV
ruta_carpeta = "superclasses"

superclasses = []

# Iterar sobre todos los archivos en la carpeta
for nombre_archivo in os.listdir(ruta_carpeta):
    # Comprobar si el elemento en la carpeta es un archivo CSV
    if nombre_archivo.endswith(".csv"):
        # Abrir y leer el contenido del archivo CSV
        with open(os.path.join(ruta_carpeta, nombre_archivo), 'r', newline='') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            # Leer cada fila del archivo CSV y agregarla al contenido de los archivos como una cadena de texto
            contenido_archivo_como_texto = "\n".join(",".join(fila) for fila in lector_csv)
            superclasses.append(contenido_archivo_como_texto)


      
def get_wikidata_uri(term):
    
    url = 'https://query.wikidata.org/sparql'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    retrieve_query = """
            SELECT * {
            ?item rdfs:label "TERM"@es.
          }
        """
    query = retrieve_query.replace("TERM", term)
    r = requests.get(url, params={'format': 'json', 'query': query}, headers=headers)
    data = r.json() 

    return data

def get_superclass(uri):
    url = 'https://query.wikidata.org/sparql'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    superclass_query = """
            SELECT ?item {
           wd:WDTID wdt:P279 ?item.
          }
        """
    print(superclass_query)
    sp_query = superclass_query.replace("WDTID", uri)
    r = requests.get(url, params={'format': 'json', 'query': sp_query}, headers=headers)
    data = r.json() 
    
    
    return data

for sentence in train_data:
    results = {}
    ident=sentence['Id']
    results['Id']=ident    
    text=sentence['Text']
    results['Text']=text

    tags=[]
    
    
    doc = nlp(text)

    for token in doc:
        if token.dep_ == "nmod" or token.dep_ == "obj" or token.dep_ == "obl":
            print(token.text, token.pos_, token.dep_, token.lemma_)
            uri_data = get_wikidata_uri(token.lemma_)
            print(uri_data)
            if len(uri_data['results']['bindings']) != 0:
                bindings=uri_data['results']['bindings']
                for i in range(len(bindings)):
                    print('ESTO ES i')
                    print(i)
                    print(bindings[i])
                    uri=bindings[i]['item']['value']
                    print('ESTO ES URI '+uri)
                    term_uri=bindings[i]['item']['value'].split("/")[-1]
                    sp_data=get_superclass(term_uri)
                    print(sp_data)
                    if len(sp_data['results']['bindings']) != 0:
                        sp_bindings=sp_data['results']['bindings']
                        for i in range(len(sp_bindings)):
                            print(i)
                            #ESTO DA ERROR
                            sp_uri=bindings[i]['item']['value']
                        
                            for item in superclasses:
                                if item == sp_uri:
                                    print('YES')
                                else:
                                    print('NO')

                    else:
                        continue
                            
            else:
                continue






uri="Q181600"
get_superclass(uri)

test = get_superclass("Q181600")
print(test)







