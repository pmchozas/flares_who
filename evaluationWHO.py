#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 18:45:48 2024

@author: pmchozas
"""
import json

resulting_data=[]
results="diccionarios.json"
train_file= "5w1h_subtarea_1_train.json" #Path to dataset
train_data=[]
with open(results, "r") as f:
  for line in f.readlines():
      result_data=json.loads(line)

with open(train_file, "r") as f:
    for line in f.readlines():
        source_data = json.loads(line)
        for tag in source_data['Tags']:
            if tag['5W1H_Label'] == "WHO":
                print(tag['Tag_Text'])
      
