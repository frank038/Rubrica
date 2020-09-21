#!/usr/bin/env python3
from shutil import copy2

def save_rubrica(data_list):
    
    ffile="data.db"
    
    if data_list:
        try:
            # make a backup of the file first
            copy2("data.db", "data.db_bk")
            
            f = open(ffile, "w")
            
            data_list.sort()
            
            for el in data_list:
                
                # replace the NoneType
                for idx, item in enumerate(el):
                    if item is None:
                        el[idx] = " "
                
                ell = ';;'.join(el)+"\n"
                
                f.write(ell)
            
            f.close()
        except:
            return 2

        return 1
    
    else:
        return 3
