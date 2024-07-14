#sql #table 

### Columns:
[[columns/collections-id|id]]
[[columns/collections-date_created|date_created]]
[[columns/collections-date_modified|date_modified]]
[[columns/collections-title|title]]
[[columns/collections-position|position]]
[[columns/collections-is_syncable|is_syncable]]
[[columns/collections-suggestion_url|suggestion_url]]
[[columns/collections-suggestion_dismissed|suggestion_dismissed]]
[[columns/collections-suggestion_type|suggestion_type]]
[[columns/collections-thumbnail|thumbnail]]
[[columns/collections-is_custom_thumbnail|is_custom_thumbnail]]
[[columns/collections-tag|tag]]
[[columns/collections-thumbnail_url|thumbnail_url]]
[[columns/collections-is_marked_for_deletion|is_marked_for_deletion]]

### Constraints:

### SQL
```sqlite
CREATE TABLE collections (
  id TEXT PRIMARY KEY,
  date_created REAL NOT NULL,
  date_modified REAL NOT NULL,
  title TEXT NOT NULL,
  position INTEGER NOT NULL,
  is_syncable INTEGER DEFAULT 1,
  suggestion_url TEXT,
  suggestion_dismissed INTEGER,
  suggestion_type INTEGER,
  thumbnail BLOB,
  is_custom_thumbnail INTEGER NOT NULL DEFAULT 0,
  tag TEXT,
  thumbnail_url TEXT,
  is_marked_for_deletion INTEGER
)
```