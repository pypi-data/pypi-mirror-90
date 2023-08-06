
Install the package using pip
`pip install editmenu`

Import **editmenu** module from **editmenu** package
 `>>>from editmenu import editmenu`
 
 Use **EditMenu** class to create an instance with a dictionary containing required values to be displayed and edited.
 `>>>mymenu = editmenu.EditMenu({"Name:"Monty","LastName":"Python"})`

Use **menu()** member function to display the menu and prompt the user to make required editing.
 `>>>mymenu.menu()`

**Notes**

 1. Grey color is used as the font color for the values and updated values will be of white. This is for distinguishing changes.
 2. As of now editmenu package is only tested on ubuntu terminal. If you face any issue on windows platform, please mention the issue on github page this package.
 3. EditMenu class, accepts only dictionary containing key:value pairs, where both key and value must be of string type.
 4. menu() function returns a dictionary with updated values.

