import enum

class Tables(enum.Enum):
    COLLECTIONS = "collections"
    ITEMS = "items"
    COLLECTIONS_SYNC = "collections_sync"
    ITEMS_SYNC = "items_sync"
    COLLECTIONS_ITEMS_RELATIONSHIP = "collections_items_relationship"
    FAVICONS = "favicons"
    META = "meta"
    COMMENTS = "comments"
    ITEMS_OFFLINE_DATA = "items_offline_data"
    COLLECTIONS_PRISM = "collections_prism"

class Collections(enum.Enum):
    ID = "id"
    DATE_CREATED = "date_created"
    DATE_MODIFIED = "date_modified"
    TITLE = "title"
    POSITION = "position"
    IS_SYNCABLE = "is_syncable"
    SUGGESTION_URL = "suggestion_url"
    SUGGESTION_DISMISSED = "suggestion_dismissed"
    SUGGESTION_TYPE = "suggestion_type"
    THUMBNAIL = "thumbnail"
    IS_CUSTOM_THUMBNAIL = "is_custom_thumbnail"
    TAG = "tag"
    THUMNAIL_URL = "thumbnail_url"
    IS_MARKED_FOR_DELETION = "is_marked_for_deletion"

class Items(enum.Enum):
    ID = "id"
    DATE_CREATED = "date_created"
    DATE_MODIFIED = "date_modified"
    TITLE = "title"
    SOURCE = "source"
    ENTITY_BLOB = "entity_blob"
    FAVICON_URL = "favicon_url"
    CANONICAL_IMAGE_DATA = "canonical_image_data"
    CANONICAL_IMAGE_URL = "canonical_image_url"
    TEXT_CONTENT = "text_content"
    HTML_CONTENT = "html_content"
    TYPE = "type"
    PROGRESSING = "progressing"
    IS_SYNCABLE = "is_syncable"
    COLOR = "color"
    THIRD_PARTY_DATA = "third_party_data"
    REMOTE_URL = "remote_url"
    TAG = "tag"
    IS_MARKED_FOR_DELETION = "is_marked_for_deletion"

class Collections_Sync(enum.Enum):
    COLLECTION_ID = "collection_id"
    IS_SYNCABLE = "is_syncable"
    SERVER_ID = "server_id"
    DATE_LAST_SYNCED = "date_last_synced"

class Items_Sync(enum.Enum):
    ITEM_ID = "item_id"
    IS_SYNCABLE = "is_syncable"
    SERVER_ID = "server_id"
    DATE_LAST_SYNCED = "date_last_synced"

class Collections_Items_Relationship(enum.Enum):
    ITEM_ID = "item_id"
    PARENT_ID = "parent_id"
    POSITION = "position"

class Favicons(enum.Enum):
    URL = "url"
    DATA = "data"

class Meta(enum.Enum):
    KEY = "key"
    VALUE = "value"

class Comments(enum.Enum):
    ID = "id"
    PARENT_ID = "parent_id"
    TEXT = "text"
    PROPERTIES = "properties"

class Items_Offline_Data(enum.Enum):
    ITEM_ID = "item_id"
    OFFLINE_FILE_DATA = "offline_file_data"
    
class Collections_Prism(enum.Enum):
    ID = "id"
    DATE_MODIFIED = "date_modified"
    TITLE = "title"