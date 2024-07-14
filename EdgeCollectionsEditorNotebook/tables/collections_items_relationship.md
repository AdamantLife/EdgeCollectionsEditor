#sql #table 

### Columns:
[[columns/collections_items_relationship-item_id|item_id]]
[[columns/collections_items_relationship-parent_id|parent_id]]
[[columns/collections_items_relationship-position|position]]

### Constraints:

### SQL
```sqlite
CREATE TABLE collections_items_relationship (
  item_id TEXT NOT NULL REFERENCES items (
    id
  ) ON DELETE CASCADE,
  parent_id TEXT NOT NULL REFERENCES collections (
    id
  ) ON DELETE CASCADE,
  position INTEGER NOT NULL
)
```