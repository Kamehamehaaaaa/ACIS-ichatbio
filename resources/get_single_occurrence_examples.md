If the user places a search term in quotes, always use the full text that is quoted, do not break it up.

If the user specifies that they want to search for an exact id, use the "id" field.

## Example 1

```
Request: "get data for id 00000002-3cef-4bc1-8540-2c20b4798855"
rq: {
    "id": "00000002-3cef-4bc1-8540-2c20b4798855"
}
```