#sql #table 

### Columns:
[[columns/collections_sync-collection_id|collection_id]]
[[columns/collections_sync-is_syncable|is_syncable]]
[[columns/collections_sync-server_id|server_id]]
[[columns/collections_sync-date_last_synced|date_last_synced]]

### Constraints:

### SQL
```sqlite
CREATE TABLE collections_sync (
  collection_id TEXT,
  is_syncable INTEGER DEFAULT 1,
  server_id TEXT NULL,
  date_last_synced REAL NULL,
  FOREIGN KEY (collection_id) REFERENCES collections (
    id
  )
)
```