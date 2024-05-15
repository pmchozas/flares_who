#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 10:24:01 2024

@author: pmchozas
"""
import json
import spacy

nlp = spacy.load('es_core_news_lg')

train_file= "5w1h_subtarea_1_train.json" #Path to dataset


text='En esos días y con dinero público, Irene Montero, la mujer de Pablo Iglesias, montaba carteles incitando a la gente a ir al aquelarre feminista en el que se contagio hasta la mujer de Sánchez'
text2='No es la primera vez que Nabarro advierte sobre los efectos adversos de las cuarentenas."'
text3='En su documento, la Conass recomendó la inmediata “prohibición de eventos presenciales como espectáculos, congresos, actividades religiosas, deportivas o similares en todo el territorio nacional”.'
text4='Los médicos ecuatorianos, dirigidos por el Doctor Jacinto Pichamaluco, desobedecieron la ley mundial de la salud OMS, de no hacer autopsias en los muertos del Coronavirus y ellos confirmaron que NO es un VIRUS sino una BACTERIA la que produce la muerte.'
text5="El cerebro del niño, o del adolescente, está sediento de oxígeno."
#text = "Los médicos ecuatorianos, dirigidos por el Doctor Jacinto Pichamaluco, desobedecieron la ley mundial de la salud OMS, de no hacer autopsias en los muertos del Coronavirus y ellos confirmaron que NO es un VIRUS sino una BACTERIA la que produce la muerte."
sujetos_nominales = []
total_results=[]
train_data= []
json_results="results.json"
testing_file="testing.json"
def ordenar_palabras_segun_texto(palabras, texto):
    # Dividir el texto en palabras y eliminar la puntuación
    palabras_texto = [palabra.strip(",.!?") for palabra in texto.split()]
    
    # Crear un conjunto para mantener un registro de las palabras ya vistas
    palabras_vistas = set()
    
    # Crear un diccionario que mapea cada palabra a su posición en el texto
    indice_palabra = {}
    for index, palabra in enumerate(palabras_texto):
        if palabra not in palabras_vistas:
            palabras_vistas.add(palabra)
            indice_palabra[palabra] = index
    
    # Ordenar las palabras de acuerdo a su posición en el texto
    palabras_ordenadas = sorted(palabras, key=lambda palabra: indice_palabra.get(palabra, float('inf')))
    
    return palabras_ordenadas

def eliminar_duplicados(lista_diccionarios):
    # Convertir cada diccionario a un conjunto de tuplas
    conjuntos = [frozenset(d.items()) for d in lista_diccionarios]
    
    # Eliminar duplicados manteniendo el orden original
    conjuntos_unicos = dict.fromkeys(conjuntos)
    
    # Convertir los conjuntos de tuplas de nuevo a diccionarios
    diccionarios_unicos = [dict(items) for items in conjuntos_unicos]
    
    return diccionarios_unicos


def obtener_indice(token):
    return token.idx    

with open(train_file, "r") as f:
  for line in f.readlines():
      train_data.append(json.loads(line))

for sentence in train_data:
    results = {}
    ident=sentence['Id']
    results['Id']=ident    
    text=sentence['Text']
    results['Text']=text

    tags=[]
    
    
    doc = nlp(text)

    for token in doc:
    
        #print(token.text, token.dep_, token.head.text)
            # Si encuentra un nsubj
        if token.dep_ == "nsubj":
            who_dict={}
            dependencies=[]
            suj_token = token.text
            dependencies.append(suj_token)
            suj_pos= token.idx
            print(suj_pos)
            print('ESTO ES EL TOKEN SUJETO: ' + suj_token)
            for otro_token in doc:
                if otro_token.head.text == suj_token and otro_token.idx < suj_pos and otro_token.dep_ != "punct":
                    print('ESTO ES DEPENDENCIA ANTES DEL SUJETO: '+otro_token.text)
                    dependencies.append(otro_token.text)
                    
                elif otro_token.text=="," and otro_token.idx > suj_pos:
                    comma_pos = otro_token.idx
                    print('ESTO ES COMMA POS: '+str(comma_pos))
                    for other in doc:
                        if other.head.text == suj_token and other.idx < comma_pos and other.text not in dependencies and other.dep_ != "punct":
                            print('DEPENDENCIA ANTES DE LA COMA: '+other.text)
                            dependencies.append(other.text)
                    break
                
            print(dependencies)
            
            ordered=ordenar_palabras_segun_texto(dependencies, text)
            print('ESTO ES ORDERED')
            print(ordered)    
            if ordered[0] in text:#cambiar text5 por sentence
                print(text.find(ordered[0]))
                start=text.find(ordered[0])
            if ordered[-1] in text:
                print(text.find(ordered[-1]))
                end=text.find(ordered[-1])+len(ordered[-1])
            chunk=text[start:end]
            doc=nlp(chunk)
            print('ESTO ES CHUNK:'+chunk)
            print(doc.text)
            who = " ".join(ordered)
            print ('ESTO ES WHO: '+who)
            print(who)
            for token in doc:
                print('ESTO ES TOKEN en CHUNK TOKENS: ')
                print(token)
                if str(token) not in who:
                    print('ESTO ES TOKEN NOT IN WHO')
                    print(token)
                    ordered.append(str(token))
                    
                else:
                    who_dict['Tag_text']=who
                    tags.append(who_dict)
                    
            #convertir lista a string
            new_ordered = ordenar_palabras_segun_texto(ordered, chunk)
            who = " ".join(new_ordered)
            who_dict['Tag_text']=who
            tags.append(who_dict)

    clean_tags=eliminar_duplicados(tags)
    results['Tags']=clean_tags
    total_results.append(results)
# with open(json_results, "w", encoding="utf-8") as file:
#     json.dump(total_results, file, ensure_ascii=False)
           


def guardar_diccionarios_separados_en_json(lista_diccionarios, nombre_archivo):
    with open(nombre_archivo, 'w', encoding="utf-8") as archivo:
        for diccionario in lista_diccionarios:
            json.dump(diccionario, archivo, ensure_ascii=False)
            archivo.write('\n')  # Agrega un salto de línea entre cada diccionario

# Ejemplo de uso
lista_diccionarios = [
    {"a": 1, "b": 2},
    {"a": 2, "b": 3},
    {"a": 3, "b": 4}
]

guardar_diccionarios_separados_en_json(total_results, "diccionarios.json")
            
            
            
#             for i, token in enumerate(doc):
#                     # Verifica si el token actual es el token objetivo
#                     if token.text == token_objetivo:
#                         # Verifica si el siguiente token es una coma
#                         posicion_coma=None
#                         for j in range(i + 1, len(doc)):
#                             # Verifica si el token actual es una coma
#                             if doc[j].text == ",":
#                                 print("Posición de la coma:", j)
                            
#                         # Si no se encontró ninguna coma después del token objetivo
#                         print("No se encontró una coma después del token objetivo.")

#             # Iteramos sobre cada token (otro_token) en la lista de tokens (sent)
#             for otro_token in first:
#                 # Verificamos si el token principal del otro_token tiene el mismo texto que el token de referencia
#                 if otro_token.head.text == token.text:
#                     # Si la condición se cumple, agregamos el texto del otro_token a la lista de dependientes
#                     dependientes.append(otro_token.text)
            
#             # Al final del bucle, dependientes contendrá los textos de los tokens dependientes del token de referencia

            
#             print(dependientes)
#             if dependientes:
#                 # Agrega el nsubj a la lista de dependientes
#                 sujeto = dependientes.copy()
#                 sujeto.append(token.text)
#                 # Ordena el sujeto nominal según el índice de los tokens
#                 sujeto.sort(key=lambda x: sent.text.index(x))
#                 sujetos_nominales.append(sujeto)
# # Imprime el resultado
# print(" ".join([" ".join(sujeto) for sujeto in sujetos_nominales]))






# for item in train_data:
#     text=item['Text']
#     doc=nlp(text)




# for entity in document.ents:
#     print('Type: {}, Value: {}, start: {}, end: {}'.format(entity.label_, entity.text,entity.start_char, entity.end_char))

# if WHO is nsubj
# dependencies=[]
# for token in document:
#     #print(token.text, token.dep_, token.head.text)
#     #print(token.text, token.dep_)
#     if token.dep_ == 'nsubj':
#         suj  = token.text
        
#         print(suj)
#         for token in document:
#             if token.head.text == suj:
                
#                 dependencies.append(token.text) 
        
#                 dependencies.append(suj)    
#                 tokens_en_frase = [token for token in document if token.text in dependencies]
        
#                 # Ordena los tokens basándose en su índice en la frase
#                 lista_tokens_ordenada = sorted(tokens_en_frase, key=lambda token: token.i)
        
#                 # Convierte los tokens ordenados de nuevo a texto si es necesario
#                 lista_tokens_ordenada_texto = [token.text for token in lista_tokens_ordenada]
                
#                 print("Lista de tokens ordenada:", lista_tokens_ordenada_texto)



        # print(token.text, token.pos_, token.i)
        # prev_token=document[token.i - 1]
        # if prev_token.dep_ =='det':
        #     who=prev_token, token

    # Texto de ejemplo


            
        
    