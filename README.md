# sensor-data-extractor

## JSON file
Edit data.json file following the example. Add separators used for a data format, add how many ids and sensor data you're fetching
```
{
    "Dfmt8020001": {
            "sep":[":"," ",","],
            "fields":{"gateway_term":{} ,"gateway":{}, "space1":{}, "device_term":{}, "device":{}, "space2":{}, "analog_term":{}, "space3":{}, "pH":{}, "tds":{}, "bat":{}, "temperature":{}}
        },
    
    "Dfmt8020002": {
        "sep":[":"," ",","],
        "fields":{"space1":{}, "gateway_term":{} ,"gateway":{}, "space2":{}, "status":{}}
    },

    "Dfmt8020003": {
        "sep":[":"," ",","],
        "fields":{"gateway_term":{} ,"gateway":{}, "space1":{}, "status":{}}
    }
            
            
}
```

## python code
Following is an example python code showing how you can fetch data according to data format

```
    ### example data
    data1 = 'GID:8020002203220000, DID:802102206290004, Analog: 1000 142 0 476'
    data2 = ' GID:8020002203220000, connected'
    data3 = 'GID:8020002203220000, connected'

    # ### data format
    dfmt1 = 'Dfmt8020001'
    dfmt2 = 'Dfmt8020002'
    dfmt3 = 'Dfmt8020003'

    ### creating object with various data format
    o1 = extractor(dfmt1, dfmt3, dfmt2)
    o2 = extractor(dfmt1, dfmt3, dfmt2)
    o3 = extractor(dfmt1, dfmt3, dfmt2)

    ### will return dictionary as defined in file.json
    dict1 = o1.__extract__(data1)
    dict2 = o2.__extract__(data2)
    dict3 = o3.__extract__(data3)

    print(dict1)
    print(dict2)
    print(dict3)
```
