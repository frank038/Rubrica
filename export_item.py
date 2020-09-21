#!/usr/bin/env python3

def export_item(data, path):
    
    for i in range(len(data)):
        if data[i] is None:
            data[i] = ""
        elif data[i] == " ":
            data[i] = ""
    
    saved_file = path+"/item.vcf"
    
    item = \
    "BEGIN:VCARD"+"\n"+\
    "VERSION:3.0"+"\n"+\
    "N:"+data[0]+";"+data[1]+";;;"+"\n"+\
    "FN:"+data[0]+" "+data[1]+"\n"+\
    "TEL;TYPE=home:"+data[2]+"\n"+\
    "EMAIL:"+data[3]+"\n"+\
    "URL:"+data[4]+"\n"+\
    "NOTE:"+data[5]+"\n"+\
    "END:VCARD"
    
    try:
        with open(saved_file, "w") as f:
            f.write(item)
    except:
        return 2
    
    return 1
