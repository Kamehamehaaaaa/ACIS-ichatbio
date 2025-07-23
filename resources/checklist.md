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