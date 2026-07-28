drop table if exists FILE;
create table FILE(
    name TEXT NOT NULL,
    hash TEXT NOT NULL,
    version INTEGER NOT NULL,
    create_timestamp INTEGER NOT NULL
);

drop table if exists LICENSE;
create table LICENSE(
    name TEXT NOT NULL,
    create_timestamp INTEGER NOT NULL,
    update_timestamp INTEGER NOT NULL
);

drop table if exists ASSET;
create table ASSET(
    name TEXT NOT NULL,
    description TEXT,
    LICENSE_ID REFERENCES LICENSE (ROWID),
    downloads INTEGER NOT NULL DEFAULT 0,
    create_timestamp INTEGER NOT NULL,
    update_timestamp INTEGER NOT NULL
);

drop table if exists AUTHOR;
create table AUTHOR(
    name TEXT NOT NULL,
    create_timestamp INTEGER NOT NULL,
    update_timestamp INTEGER NOT NULL
);

drop table if exists ASSET_PACK;
create table ASSET_PACK(
    name TEXT NOT NULL,
    description TEXT,
    version TEXT,
    create_timestamp INTEGER NOT NULL,
    update_timestamp INTEGER NOT NULL
);

drop table if exists TAG;
create table TAG(
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    create_timestamp INTEGER NOT NULL,
    update_timestamp INTEGER NOT NULL
);


-- RELATIONS

drop table if exists REL_FILE_ASSET;
create table REL_FILE_ASSET(
    FILE_ID REFERENCES FILE (ROWID),
    ASSET_ID REFERENCES ASSET (ROWID),
    is_current INTEGER NOT NULL,
    create_timestamp INTEGER NOT NULL,
    update_timestamp INTEGER NOT NULL
);

drop table if exists REL_TAG_ASSET;
create table REL_TAG_ASSET(
    TAG_ID REFERENCES TAG (ROWID),
    ASSET_ID REFERENCES ASSET (ROWID),
    create_timestamp INTEGER NOT NULL,
    PRIMARY KEY (TAG_ID, ASSET_ID)
);

drop table if exists REL_ASSET_AUTHOR;
create table REL_ASSET_AUTHOR(
    ASSET_ID REFERENCES ASSET (ROWID),
    AUTHOR_ID REFERENCES AUTHOR (ROWID),
    create_timestamp INTEGER NOT NULL,
    PRIMARY KEY (ASSET_ID, AUTHOR_ID)
);

drop table if exists REL_ASSET_ASSET_PACK;
create table REL_ASSET_ASSET_PACK(
    ASSET_ID REFERENCES ASSET (ROWID),
    ASSET_PACK_ID REFERENCES ASSET_PACK (ROWID),
    create_timestamp INTEGER NOT NULL,
    PRIMARY KEY (ASSET_ID, ASSET_PACK_ID)
);
