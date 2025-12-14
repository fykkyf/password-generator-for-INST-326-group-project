# password-generator-for-INST-326-group-project
INST 326 group project

FILES:
PasswordDictionary.py
A dictionary file for "PasswordGenerator.py", provides the letters and special characters for password generation. 

PasswordGenerator.py
The file which generates passwords when prompted in the main file. "PasswordDictionary.py" is required for it to function.

PasswordManager.py
The file which manages password entries using SQLite for storage. Uses Pandas for viewing, importing, and exporting password data.

PasswordStrenghChecker.py
The file which checks your password and determines its strength when entered into the storage database. 

main.py
The program which uses all three classes together to generate, store, manage, strength check, and export data. Requires each of the previous python files to function. 

TestPasswordGenerator.py & TestPasswordStrengthChecker.py
Files which use pytest to test functions.


HOW 2 RUN:
Install each of the given files, make sure they are all in the same folder. You can run the program with either VS code or straight in your terminal. Python 3.13 is required.
When ran the program will present you with 9 possible options to chose from. simply type any number provided and the chosen choice will run. The program will prompt you for any additional input required.
