#sql #table 

### Columns:
[[columns/comments-id|id]]
[[columns/comments-parent_id|parent_id]]
[[columns/comments-text|text]]
[[columns/comments-properties|properties]]

### Constraints:

### SQL
```sqlite
CREATE TABLE comments (
  id TEXT PRIMARY KEY,
  parent_id TEXT NOT NULL,
  text TEXT NOT NULL,
  properties BLOB,
  FOREIGN KEY (parent_id) REFERENCES items (
    id
  ) ON DELETE CASCADE
)
```