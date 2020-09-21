#!/usr/bin/env python3

def export_all(data_list, path):
    saved_file = path+"/rubrica.vcf"
    
    def create_item(data):
        item = \
        "BEGIN:VCARD"+"\n"+\
        "VERSION:3.0"+"\n"+\
        "N:"+data[0]+";"+data[1]+";;;"+"\n"+\
        "FN:"+data[0]+" "+data[1]+"\n"+\
        "TEL;TYPE=home:"+data[2]+"\n"+\
        "EMAIL:"+data[3]+"\n"+\
        "URL:"+data[4]+"\n"+\
        "NOTE:"+data[5]+"\n"+\
        "END:VCARD"+"\n\n"
        
        return item
    
    def clean_record(data):
        for i in range(len(data)):
            if data[i] is None:
                data[i] = ""
            elif data[i] == " ":
                data[i] = ""
        return data
    
    try:
        f = open(saved_file, "w")
        
        for el in data_list:
            # some cleaning
            cleaned_item = clean_record(el)
            # prepare the item
            item_to_write = create_item(cleaned_item)
            #
            f.write(item_to_write)
        f.close()
    except:
        return 2
    
    return 1
