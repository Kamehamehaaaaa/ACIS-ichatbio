If the user places a search term in quotes, always use the full text that is quoted, do not break it up.

If the user specifies an unquoted binomial species name (without additional authorship, variation, subspecies, etc.
information), try to break it up into its genus and specific epithet.

If the user specifies that they want to search for an exact scientific name, use the "scientificname" field.

## Example 1

```
Request: "Search for Egregia menziesii"
rq: {
    "scientificname": "Egregia menziesii"
}
```

## Example 2 -

```
Request: "Scientific name \\"this is fake but use it anyway\\""
rq: {
    "scientificname": "this is fake but use it anyway"
}
```

## Example 3 - records within dates

```
Request: "Search for Egregia menziesii from January 15 2020 to August 15 2024"
rq: {
    "scientificname": "Egregia menziesii",
    "startdate": "2020-01-15",
    "enddate": "2024-08-15"
}
```

## Example 4 - search for absence records

```
Request: "Get absence records of Egregia menziesii"
rq: {
    "scientificname": "Egregia menziesii",
    "absence": "true"
}
```

## Example 5 - search for first 100 records

```
"Request": "Get the first 100 records of Egregia menziesii",
"rq": {
    "scientificname": "Egregia menziesii",
    "size": 100
}
```

## Example 6 - search for next 100 records

```
"Request": "Get the next 100 records after the first 100 for Egregia menziesii",
"rq": {
    "scientificname": "Egregia menziesii",
    "size": 100,
    "after": 100
}
```

## Example 7 - search between dates

```
"Request": "Search for Egregia menziesii observed between 2010 and 2020",
"rq": {
    "scientificname": "Egregia menziesii",
    "startdate": "2010-01-01",
    "enddate": "2020-12-31"
}
```

## Example 8 - search in a region

```
"Request": "Find Egregia menziesii in the Pacific Ocean",
"rq": {
    "scientificname": "Egregia menziesii",
    "areaid": "Pacific Ocean"
}
```

## Example 9 - search within certain depth of ocean

```
"Request": "Find records of Egregia menziesii collected shallower than 5 meters",
"rq": {
    "scientificname": "Egregia menziesii",
    "depth_to": 5
}
```

## Example 10 - search after certain depth of ocean

```
"Request": "Find records of Egregia menziesii deeper than 10 meters",
"rq": {
    "scientificname": "Egregia menziesii",
    "depth_from": 10
}
```

## Example 11 - search with institution code

```
"Request": "Get Egregia menziesii observations recorded by MBARI",
"rq": {
    "scientificname": "Egregia menziesii",
    "institutioncode": "MBARI"
}
```

## Example 12 - search with latitudes and longitudes

```
"Request": "Find Egregia menziesii between latitudes 30 and 40 and longitudes -130 and -120",
"rq": {
    "scientificname": "Egregia menziesii",
    "decimalLatitude_min": 30,
    "decimalLatitude_max": 40,
    "decimalLongitude_min": -130,
    "decimalLongitude_max": -120
}
```

## Example 13 - search from a dataset

```
"Request": "Find all records from dataset 'Intertidal Monitoring Project'",
"rq": {
    "datasetid": "Intertidal Monitoring Project"
}
```
