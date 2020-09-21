# Rubrica
A simple programs to collect contacts. Version 1.1

rubrica_20200921_b.tar.gz: MD5SUM 90830d1921a9a1ea0c6642964bf38f33

Each field can be filled by clicking again into the selected row.
The buttons from the left:
- insert a new record
- delete the selected record (a confirmation dialog should appear)
- save the database (into a plain text in the same forlder of the program)
- export the selected item (into a vcf file)
- export the whole database (into a single vcf file)
- import a vcf file (only selected fields will be parsed)
- exit the program (a dialog should appear if the database has been changed).

The button on the left
Each button filter the whole list using the first character of the first field of each row.
The first field, Surname/Co., is mandatory. If empty, an arbitrary character will be used.
The button with label "@" reset the filter and all the database will be shown.
Some buttons can be pressed only when no filter is used.

Import and export of the vcf file
This program parses only the following fields:
- surname
- name
- telephone (even more than one field while importing)
- email (even more than one field while importing)
- url (even more than one field while importing)
- note.

Configuration file
Only three option to change manually:
- width of the program
- height of the program
- use (1) or not use (0) the headbar.

Screenshots:
without headbar
![My image](https://github.com/frank038/Rubrica/blob/master/Image1.png)
with headbar
![My image](https://github.com/frank038/Rubrica/blob/master/Image2.png)
