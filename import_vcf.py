#!/usr/bin/env python3

def import_vcf(file):
    
    data_list = []
    
    temp_list = []
    
    temp_record_surname = ""
    temp_record_name = ""
    temp_record_tel = ""
    temp_record_email = ""
    temp_record_url = ""
    temp_record_note = ""
    
    marker = 0
    
    try:
        # fields recognized: Surname, Name, Telephone, Email, Url, Note
        with open(file, "r") as f:
            line = f.readline()
            
            while line:
                
                if line.strip("\n") == "BEGIN:VCARD":
                    marker = 1
                elif line.strip("\n") == "END:VCARD" and marker == 1:
                    temp_list.append(temp_record_surname)
                    temp_list.append(temp_record_name)
                    temp_list.append(temp_record_tel[:-1])
                    temp_list.append(temp_record_email[:-1])
                    temp_list.append(temp_record_url[:-1])
                    temp_list.append(temp_record_note)
                    data_list.append(temp_list)
                    temp_list = []
                    temp_record_surname = ""
                    temp_record_name = ""
                    temp_record_tel = ""
                    temp_record_email = ""
                    temp_record_url = ""
                    temp_record_note = ""
                    marker = 0
                elif marker == 1:
                    # surname and name - surname is mandatory
                    if line.strip()[0:2] == "N:":
                        temp_a = line.strip().split(":")
                        temp_b = temp_a[1]
                        temp_data = temp_b.split(";")
                        surname = temp_data[0].strip()
                        if surname == "" or surname == " " or surname == None:
                            surname = "MISSED"
                        if not (surname[0].isalpha() or surname.isdecimal()):
                            surname = "A"+surname[1:]
                        name = temp_data[1]
                        temp_record_surname = surname
                        temp_record_name = name
                    # telephone
                    elif line.strip()[0:3] == "TEL":
                        temp_a = line.strip().split(":")
                        telephone = temp_a[-1]
                        temp_record_tel += telephone+" "
                    # email
                    elif line.strip()[0:5] == "EMAIL":
                        temp_a = line.strip().split(":")
                        email = temp_a[-1]
                        temp_record_email += email+" "
                    # url
                    elif line.strip()[0:3] == "URL":
                        temp_a = line.strip().split(":")
                        print(temp_a)
                        if temp_a[-2] in ["https", "http", "HTTPS", "HTTP"]:
                            url = temp_a[-2]+":"+temp_a[-1]
                        else:
                            url = temp_a[-1]
                        temp_record_url += url+" "
                    # note
                    elif line.strip()[0:4] == "NOTE":
                        temp_a = line.strip().split(":")
                        temp_b = temp_a[1]
                        note = temp_b
                        temp_record_note = note
                
                line = f.readline()
                
    except:
        return 2
    
    return data_list
