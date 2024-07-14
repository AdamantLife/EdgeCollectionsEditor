#sql #table 

### Columns:
[[columns/favicons-url|url]]
[[columns/favicons-data|data]]

### Constraints:

### SQL
```sqlite
CREATE TABLE favicons (
  url TEXT PRIMARY KEY,
  data BLOB
)
```