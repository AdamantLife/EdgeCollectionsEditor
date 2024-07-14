#sql #table 

### Columns:
[[columns/items_sync-item_id|item_id]]
[[columns/items_sync-is_syncable|is_syncable]]
[[columns/items_sync-server_id|server_id]]
[[columns/items_sync-date_last_synced|date_last_synced]]

### Constraints:

### SQL
```sqlite
CREATE TABLE items_sync (
  item_id TEXT,
  is_syncable INTEGER DEFAULT 1,
  server_id TEXT NULL,
  date_last_synced REAL NULL,
  FOREIGN KEY (item_id) REFERENCES items (
    id
  )
)
```