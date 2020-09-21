# Rubrica
A simple programs to collect contacts.

rubrica_20200921.tar.gz: MD5SUM b518a4333b5e633f813e8ced17375bb3

Each field can be filled by clicking again into the selected row.
The buttons from the left:
- insert a new record
- delete the selected record (a confirmation dialog should appear)
- save the database (into a plain text in the same forlder of the program)
- export the selected item (into a vcf file)
- export the whole database (into a single vcf file)
- import a vcf file (only selected fields will be parsed)
- exit the program (a dialog should appear if the database has been changed).

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
