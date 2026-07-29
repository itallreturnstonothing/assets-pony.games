drop table if exists LICENSE;
create table LICENSE(
    LICENSE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    create_timestamp INTEGER NOT NULL DEFAULT (unixepoch()),
    update_timestamp INTEGER NOT NULL DEFAULT (unixepoch())
);

drop table if exists ASSET;
create table ASSET(
    ASSET_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    LICENSE_ID REFERENCES LICENSE (LICENSE_ID),
    downloads INTEGER NOT NULL DEFAULT 0,
    create_timestamp INTEGER NOT NULL DEFAULT (unixepoch()),
    update_timestamp INTEGER NOT NULL DEFAULT (unixepoch())
);

drop table if exists AUTHOR;
create table AUTHOR(
    AUTHOR_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    create_timestamp INTEGER NOT NULL DEFAULT (unixepoch()),
    update_timestamp INTEGER NOT NULL DEFAULT (unixepoch())
);

drop table if exists ASSET_PACK;
create table ASSET_PACK(
    ASSET_PACK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    version TEXT,
    create_timestamp INTEGER NOT NULL DEFAULT (unixepoch()),
    update_timestamp INTEGER NOT NULL DEFAULT (unixepoch())
);

drop table if exists TAG;
create table TAG(
    TAG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    create_timestamp INTEGER NOT NULL DEFAULT (unixepoch()),
    update_timestamp INTEGER NOT NULL DEFAULT (unixepoch())
);

drop table if exists DOWNLOAD_LINK;
create table DOWNLOAD_LINK(
    DOWNLOAD_LINK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    is_active INTEGER,
    latest_active_timestamp INTEGER,
    create_timestamp INTEGER NOT NULL DEFAULT (unixepoch()),
    update_timestamp INTEGER NOT NULL DEFAULT (unixepoch())
);

-- RELATIONS

drop table if exists REL_TAG_ASSET;
create table REL_TAG_ASSET(
    TAG_ID REFERENCES TAG (TAG_ID),
    ASSET_ID REFERENCES ASSET (ASSET_ID),
    create_timestamp INTEGER NOT NULL DEFAULT (unixepoch()),
    PRIMARY KEY (TAG_ID, ASSET_ID)
);

drop table if exists REL_ASSET_AUTHOR;
create table REL_ASSET_AUTHOR(
    ASSET_ID REFERENCES ASSET (ASSET_ID),
    AUTHOR_ID REFERENCES AUTHOR (AUTHOR_ID),
    create_timestamp INTEGER NOT NULL DEFAULT (unixepoch()),
    PRIMARY KEY (ASSET_ID, AUTHOR_ID)
);

drop table if exists REL_ASSET_ASSET_PACK;
create table REL_ASSET_ASSET_PACK(
    ASSET_ID REFERENCES ASSET (ASSET_ID),
    ASSET_PACK_ID REFERENCES ASSET_PACK (ASSET_PACK_ID),
    create_timestamp INTEGER NOT NULL DEFAULT (unixepoch()),
    PRIMARY KEY (ASSET_ID, ASSET_PACK_ID)
);

drop table if exists REL_ASSET_DOWNLOAD_LINK;
create table REL_ASSET_DOWNLOAD_LINK(
    ASSET_ID REFERENCES ASSET (ASSET_ID),
    DOWNLOAD_LINK_ID REFERENCES DOWNLOAD_LINK (DOWNLOAD_LINK_ID),
    create_timestamp INTEGER NOT NULL DEFAULT (unixepoch()),
    PRIMARY KEY (ASSET_ID, DOWNLOAD_LINK_ID)
);
