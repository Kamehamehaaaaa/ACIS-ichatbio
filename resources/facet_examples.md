# OBIS API Examples – Facets Required

## Example 1
```
Request: "Search for Egregia menziesii"
rq: {
    "facets": "originalScientificName",
    "scientificname": "Egregia menziesii"
}
```

## Example 2
```
Request: "Search for taxa with AphiaID 12345"
rq: {
    "facets": "originalScientificName",
    "taxonid": "12345"
}
```

## Example 3
```
Request: "Search for area ID A1"
rq: {
    "facets": "originalScientificName",
    "areaid": "A1"
}
```

## Example 4
```
Request: "Search for dataset with UUID 550e8400-e29b-41d4-a716-446655440000"
rq: {
    "facets": "originalScientificName",
    "datasetid": "550e8400-e29b-41d4-a716-446655440000"
}
```

## Example 5
```
Request: "Search for node UUID 123e4567-e89b-12d3-a456-426614174000"
rq: {
    "facets": "originalScientificName",
    "nodeid": "123e4567-e89b-12d3-a456-426614174000"
}
```

## Example 6
```
Request: "Search between 2020-01-01 and 2020-12-31"
rq: {
    "facets": "originalScientificName",
    "startdate": "2020-01-01",
    "enddate": "2020-12-31"
}
```

## Example 7
```
Request: "Search between depths 0 to 50 meters"
rq: {
    "facets": "originalScientificName",
    "startdepth": 0,
    "enddepth": 50
}
```

## Example 8
```
Request: "Search within geometry POLYGON((-10 40, -10 50, 0 50, 0 40, -10 40))"
rq: {
    "facets": "originalScientificName",
    "geometry": "POLYGON((-10 40, -10 50, 0 50, 0 40, -10 40))"
}
```

## Example 9
```
Request: "Search for Red List species"
rq: {
    "facets": "originalScientificName",
    "redlist": true
}
```

## Example 10
```
Request: "Search for HAB species"
rq: {
    "facets": "originalScientificName",
    "hab": true
}
```

## Example 11
```
Request: "Search for WRiMS species"
rq: {
    "facets": "originalScientificName",
    "wrims": true
}
```

## Example 12
```
Request: "Include dropped records"
rq: {
    "facets": "originalScientificName",
    "dropped": "include"
}
```

## Example 13
```
Request: "Get absence records only"
rq: {
    "facets": "originalScientificName",
    "absence": "true"
}
```

## Example 14
```
Request: "Search with quality flags 'flag1,flag2'"
rq: {
    "facets": "originalScientificName",
    "flags": "flag1,flag2"
}
```

## Example 15
```
Request: "Exclude quality flags 'flag3,flag4'"
rq: {
    "facets": "originalScientificName",
    "exclude": "flag3,flag4"
}
```

