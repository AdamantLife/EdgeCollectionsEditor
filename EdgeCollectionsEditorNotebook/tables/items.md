#sql #table 

### Columns:
[[columns/items-id|id]]
[[columns/items-date_created|date_created]]
[[columns/items-date_modified|date_modified]]
[[columns/items-title|title]]
[[columns/items-source|source]]
[[columns/items-entity_blob|entity_blob]]
[[columns/items-favicon_url|favicon_url]]
[[columns/items-canonical_image_data|canonical_image_data]]
[[columns/items-canonical_image_url|canonical_image_url]]
[[columns/items-text_content|text_content]]
[[columns/items-html_content|html_content]]
[[columns/items-type|type]]
[[columns/items-progressing|progressing]]
[[columns/items-is_syncable|is_syncable]]
[[columns/items-color|color]]
[[columns/items-third_party_data|third_party_data]]
[[columns/items-remote_url|remote_url]]
[[columns/items-tag|tag]]
[[columns/items-is_marked_for_deletion|is_marked_for_deletion]]

### Constraints:

### SQL
```sqlite
CREATE TABLE items (
  id TEXT PRIMARY KEY,
  date_created REAL NOT NULL,
  date_modified REAL NOT NULL,
  title TEXT,
  source BLOB,
  entity_blob BLOB,
  favicon_url TEXT REFERENCES favicons (
    url
  ) ON DELETE CASCADE,
  canonical_image_data BLOB,
  canonical_image_url TEXT,
  text_content TEXT,
  html_content TEXT,
  type TEXT,
  progressing INTEGER,
  is_syncable INTEGER DEFAULT 1,
  color TEXT,
  third_party_data BLOB,
  remote_url TEXT,
  tag TEXT,
  is_marked_for_deletion INTEGER
)
```