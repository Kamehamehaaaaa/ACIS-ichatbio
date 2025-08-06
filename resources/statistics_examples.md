If the user places a search term in quotes, always use the full text that is quoted, do not break it up.

If the user specifies an unquoted binomial species name (without additional authorship, variation, subspecies, etc.
information), try to break it up into its genus and specific epithet.

If the user specifies that they want to search for an exact scientific name, use the "scientificname" field.

## Example 1
Request: "Search for Egregia menziesii"
```
rq: {
    "scientificname": "Egregia menziesii"
}
```

## Example 2
Request: "Filter by AphiaID 123456"
```
rq: {
    "taxonid": "123456"
}
```

## Example 3
Request: "Get data from dataset UUID abcd-1234"
```
rq: {
    "datasetid": "abcd-1234"
}
```

## Example 4
Request: "Search data in area A123"
```
rq: {
    "areaid": "A123"
}
```

## Example 5
Request: "Show results from node UUID node-xyz"
```
rq: {
    "nodeid": "node-xyz"
}
```

## Example 6
Request: "Get occurrences recorded after Jan 1, 2020"
```
rq: {
    "startdate": "2020-01-01"
}
```

## Example 7
Request: "Get occurrences before December 31, 2023"
```
rq: {
    "enddate": "2023-12-31"
}
```

## Example 8
Request: "Show observations from depth 50m and deeper"
```
rq: {
    "startdepth": 50
}
```

## Example 9
Request: "Only show data from depths shallower than 200 meters"
```
rq: {
    "enddepth": 200
}
```

## Example 10
Request: "Filter by geometry: a rectangle off California"
```
rq: {
    "geometry": "POLYGON((-125 35, -120 35, -120 40, -125 40, -125 35))"
}
```

## Example 11
Request: "Only show Red List species"
```
rq: {
    "redlist": true
}
```

## Example 12
Request: "Only include HAB species"
```
rq: {
    "hab": true
}
```

## Example 13
Request: "Only show WRiMS species"
```
rq: {
    "wrims": true
}
```

## Example 14
Request: "Include dropped records"
```
rq: {
    "dropped": "include"
}
```

## Example 15
Request: "Show only dropped records"
```
rq: {
    "dropped": "true"
}
```

## Example 16
Request: "Include absence records"
```
rq: {
    "absence": "include"
}
```

## Example 17
Request: "Show only absence records"
```
rq: {
    "absence": "true"
}
```

## Example 18
Request: "Filter only records flagged as outliers or geospatial issues"
```
rq: {
    "flags": "outlier,geospatial"
}
```

## Example 19
Request: "Exclude records with quality flag 'depth_exceeds_range'"
```
rq: {
    "exclude": "depth_exceeds_range"
}
```

## Example 20
Request: "Find Egregia menziesii records from depths shallower than 50m after 2020"
```
rq: {
    "scientificname": "Egregia menziesii",
    "startdate": "2020-01-01",
    "enddepth": 50
}
```

## Example 21
Request: "Show WRiMS species in dataset abcd-1234 recorded between 2015 and 2022"
```
rq: {
    "datasetid": "abcd-1234",
    "wrims": true,
    "startdate": "2015-01-01",
    "enddate": "2022-12-31"
}
```

## Example 22
Request: "Get Red List and HAB species in area A999 flagged as outliers"
```
rq: {
    "areaid": "A999",
    "redlist": true,
    "hab": true,
    "flags": "outlier"
}
```

## Example 23
Request: "Search AphiaID 123456 within California coastal polygon, excluding depth errors"
```
rq: {
    "taxonid": "123456",
    "geometry": "POLYGON((-125 35, -120 35, -120 40, -125 40, -125 35))",
    "exclude": "depth_exceeds_range"
}
```

## Example 24
Request: "Include dropped absence records for HAB species from 2010 to 2020"
```
rq: {
    "hab": true,
    "dropped": "include",
    "absence": "include",
    "startdate": "2010-01-01",
    "enddate": "2020-12-31"
}
```

## Example 25
Request: "Show data from node node-xyz for Red List species flagged as geospatial outliers"
```
rq: {
    "nodeid": "node-xyz",
    "redlist": true,
    "flags": "geospatial"
}
```