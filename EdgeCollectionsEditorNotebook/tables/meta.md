#sql #table 

### Columns:
[[columns/meta-key|key]]
[[columns/meta-value|value]]

### Constraints:

### SQL
```sqlite
CREATE TABLE meta (
  key TEXT NOT NULL UNIQUE PRIMARY KEY,
  value TEXT
)
```