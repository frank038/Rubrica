#!/usr/bin/env python3

def export_all(data_list, path):
    saved_file = path+"/rubrica.csv"
    
    def clean_record(data):
        for i in range(len(data)):
            if data[i] is None:
                data[i] = " "
            elif data[i] == " ":
                data[i] = " "
            elif data[i] == "":
                data[i] = " "
        return data
    
    def create_item(data):
        item = data[0]+","+data[1]+","+data[2]+","+data[3]+","+data[4]+","+data[5]+"\n"
        return item

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
