CREATE TABLE collections (
    id LONGVARCHAR PRIMARY KEY,
    date_created REAL NOT NULL,
    date_modified REAL NOT NULL,
    title LONGVARCHAR NOT NULL,
    position INTEGER NOT NULL,
    is_syncable INTEGER DEFAULT 1,
    suggestion_url LONGVARCHAR,
    suggestion_dismissed INTEGER,
    suggestion_type INTEGER,
    thumbnail BLOB,
    is_custom_thumbnail INTEGER NOT NULL DEFAULT 0,
    tag LONGVARCHAR,
    thumbnail_url LONGVARCHAR,
    is_marked_for_deletion INTEGER
    );

CREATE TABLE items (
    id LONGVARCHAR PRIMARY KEY,
    date_created REAL NOT NULL,
    date_modified REAL NOT NULL,
    title LONGVARCHAR,
    source BLOB,
    entity_blob BLOB,
    favicon_url LONGVARCHAR REFERENCES favicons(url) ON DELETE CASCADE,
    canonical_image_data BLOB,
    canonical_image_url LONGVARCHAR,
    text_content LONGVARCHAR,
    html_content LONGVARCHAR,
    type LONGVARCHAR,
    progressing INTEGER,
    is_syncable INTEGER DEFAULT 1,
    color LONGVARCHAR,
    third_party_data BLOB,
    remote_url LONGVARCHAR,
    tag LONGVARCHAR,
    is_marked_for_deletion INTEGER
    );

CREATE TABLE collections_sync (
    collection_id LONGVARCHAR,
    is_syncable INTEGER DEFAULT 1,
    server_id LONGVARCHAR NULL,
    date_last_synced REAL NULL,
    FOREIGN KEY(collection_id) REFERENCES collections(id)
    );

CREATE TABLE items_sync (
    item_id LONGVARCHAR,
    is_syncable INTEGER DEFAULT 1,
    server_id LONGVARCHAR NULL,
    date_last_synced REAL NULL,
    FOREIGN KEY(item_id) REFERENCES items(id)
    );

CREATE TABLE collections_items_relationship (
    item_id LONGVARCHAR NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    parent_id LONGVARCHAR NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    position INTEGER NOT NULL
    );

CREATE TABLE favicons (
    url LONGVARCHAR PRIMARY KEY,
    data BLOB
    );

CREATE TABLE meta(
    key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY,
    value LONGVARCHAR
    );

CREATE TABLE comments (
    id LONGVARCHAR PRIMARY KEY,
    parent_id LONGVARCHAR NOT NULL,
    text LONGVARCHAR NOT NULL,
    properties BLOB,
    FOREIGN KEY (parent_id) REFERENCES items(id) ON DELETE CASCADE
    );

CREATE TABLE items_offline_data (
    item_id LONGVARCHAR NOT NULL REFERENCES items(id) ON DELETE CASCADE PRIMARY KEY,
    offline_file_data LONGVARCHAR NOT NULL
    );

CREATE TABLE collections_prism (
    id LONGVARCHAR PRIMARY KEY,
    date_modified REAL NOT NULL,
    title LONGVARCHAR NOT NULL
    )
