#!/usr/bin/env python3
import os

def open_rubrica():

    # rubrica
    rubrica = "data.db"
    
    file_cont2 = []
    file_cont = []
    
    if not os.path.exists(rubrica):
        try:
            f = open("data.db", "w")
            f.write("NEW RECORD;; ;; ;; ;; ;; ")
            f.close()
        except:
            return 3

    try:
        with open(rubrica, "r") as f:
            file_cont2 = f.readlines()
        
        file_cont = tuple(file_cont2)
        
        final_list = []
        
        for i in range(len(file_cont)):
            arr1 = file_cont[i].strip(";\n").split(";;")
            
            if arr1 not in [[""],["\n"]]:
                final_list.append(tuple(arr1))
    except:
        return 2
    
    return final_list
