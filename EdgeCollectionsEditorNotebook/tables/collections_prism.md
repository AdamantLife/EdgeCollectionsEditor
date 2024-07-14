#sql #table 

### Columns:
[[columns/collections_prism-id|id]]
[[columns/collections_prism-date_modified|date_modified]]
[[columns/collections_prism-title|title]]

### Constraints:

### SQL
```sqlite
CREATE TABLE collections_prism (
  id TEXT PRIMARY KEY,
  date_modified REAL NOT NULL,
  title TEXT NOT NULL
)
```