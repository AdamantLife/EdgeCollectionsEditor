#sql #table 

### Columns:
[[columns/items_offline_data-item_id|item_id]]
[[columns/items_offline_data-offline_file_data|offline_file_data]]

### Constraints:

### SQL
```sqlite
CREATE TABLE items_offline_data (
  item_id TEXT NOT NULL REFERENCES items (
    id
  ) ON DELETE CASCADE PRIMARY KEY,
  offline_file_data TEXT NOT NULL
)
```