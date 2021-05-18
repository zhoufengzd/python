# basic data pattern for data consumption
* https://pythonguide.readthedocs.io/en/latest/

## read input
* csv or json
* error checked?
    * missing value
    * wrong type
* type converted?
* proto type:
```
class DataReader():
    def read(DataClassT, init_map):
        pass
```

## build relationships
* row or json dictionary to data objects

## some calculations
