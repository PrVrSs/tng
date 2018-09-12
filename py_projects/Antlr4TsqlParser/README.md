# Antlr4TsqlParser

**CLI**

$ pip3 install cmd2

$ python3 CliTsqlParser.py

Usage: parse [options] arg

Options:

    -h, --help         show this help message and exit
    -t, --time         show time
    -f, --file         indicate file
    -j, --json         show json
    -l, --lisp_string  show lisp_string
    -s, --string       show string
    -k, --tokens       show tokens
    -a, --as_line      show as_line
  
  
Данные могут считываться с консоли или из файла, для чтения из файла требуется указать флаг -f

Пример использования

`(Cmd) parse -t -j SELECT c1,c2 FROM tab1`

`time 0.60 sec`

`{`

    "Column": [
        "c2",
        "c1"
    ],
    "Table": [
        "tab1"
    ],
    "DB": []
`}`

`(Cmd) parse -j -f input.txt`

`{`

    "DB": [
        "AdventureWorks2012;"
    ],
    "Table": [
        "Sales.SalesTerritory",
        "AdventureWorks2012.HumanResources.Employee",
        "Purchasing.Vendor",
        "pv",
        "Person.Person",
        "v",
        "Purchasing.ProductVendor",
        "Production.Product",
        "Sales.SalesPerson",
        "AdventureWorks2012.HumanResources.vEmployee"
    ],
    "Column": [
        "abc",
        "VendorID",
        "v.ProductID",
        "Name",
        "LastName",
        "EmployeeID",
        "PreferredVendorStatus",
        "v.Name",
        "pv.ProductID",
        "pv.VendorID",
        "Title",
        "FirstName"
    ]
`}`

**RestApi**

$ pip3 install flask

$ python3 RestApiTsqlParser.py


Пример использования

    $ curl -i -X GET http://localhost:5000/tasks - получение информации о ресурсе
    $ curl -i -X GET http://localhost:5000/tasks/1 - получение информации о ресурсе
    $ curl -i -X GET http://localhost:5000/tasks/1/tokens - получение информации о ресурсе
    $ curl -i -H "Content-Type: application/json" -X POST -d '{"request":"SELECTf c1,c2 FROM tab2"}' http://localhost:5000/tasks - создание ресурса
    $ curl -i -H "Content-Type: application/json" -X PUT -d '{"request":"SELECT c1,c2 FROM tab2"}' http://localhost:5000/tasks/2 - обновление ресурса
    $ curl -i -X DELETE http://localhost:5000/tasks/2 - удаление ресурса