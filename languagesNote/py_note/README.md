
# list of python special methods



### Basics


 write                 | python calls            | you want
:---------------------:|:-----------------------:| :----------------------------------------:
x = MyClass()          |x.__init__()             | to initialize an instance
repr(x)                |x.__repr__()             | the “official” representation as a string
str(x)                 |x.__str__()              | the “informal” value as a string
bytes(x)               |x.__bytes__()            | the “informal” value as a byte array
format(x, format_spec) |x.__format__(format_spec)| the value as a formatted string


### Classes That Act Like Iterators


### Computed Attributes





### Источники 
* special methods
    * http://www.diveintopython3.net/special-method-names.html
    * https://www.ibm.com/developerworks/ru/library/l-python_part_7/in%D1%81dex.html
    
* useful lib
    * 1
    * 2