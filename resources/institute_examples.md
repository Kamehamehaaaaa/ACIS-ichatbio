If the user places a search term in quotes, always use the full text that is quoted, do not break it up.

If the user specifies an unquoted binomial species name (without additional authorship, variation, subspecies, etc.
information), try to break it up into its genus and specific epithet.

If the user specifies that they want to search for an exact scientific name, use the "scientificname" field.

## Example 1

```
Request: "Search for Panthera leo records"
rq: {
    "scientificname": "Panthera leo",
}
```

## Example 2

```
Request: "Records from area ID 67890 in 2020"
rq: {
    "areaid": "67890",
    "startdate": "2020-01-01",
    "enddate": "2020-12-31",
}
```

## Example 3

```
Request: "WRiMS species only with quality flag 'verified'"
rq: {
    "wrims": true,
    "flags": ["verified"],
}
```

## Example 4

```
Request: "Red List HAB species between 5 and 200 meters"
rq: {
    "redlist": true,
    "hab": true,
    "startdepth": 5,
    "enddepth": 200,
}
```

## Example 5

```
Request: "Dropped records for taxon AphiaID 12345"
rq: {
    "taxonid": "12345",
    "dropped": "true",
}
```

## Example 6

```
Request: "Absence records in dataset UUID 550e8400-e29b-41d4-a716-446655440000"
rq: {
    "datasetid": "550e8400-e29b-41d4-a716-446655440000",
    "absence": "true",
}
```

## Example 7

```
Request: "Geometry search using GeoHash dr5ru"
rq: {
    "geometry": "dr5ru",
}
```