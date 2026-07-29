import sqlite3
import pandas as pd

#%%

df_assets = pd.read_excel("assets.ods")

#%%

with sqlite3.connect("../test.sqlite3") as conn:
    conn.execute("PRAGMA foreign_keys=ON")
    lk_tags = dict(conn.execute("select name, TAG_ID from TAG").fetchall())
    lk_authors = dict(conn.execute("select name, AUTHOR_ID from AUTHOR").fetchall())
    lk_asset_packs = dict(conn.execute("select name, ASSET_PACK_ID from ASSET_PACK").fetchall())
    
    link_1_id = conn.execute("select DOWNLOAD_LINK_ID from DOWNLOAD_LINK where url = 'https://mega.nz/folder/yKIGFSSS#148P2r8dwZlNSoCLVMKbKw'").fetchone()[0]
    link_2_id = conn.execute("select DOWNLOAD_LINK_ID from DOWNLOAD_LINK where url = 'https://drive.google.com/drive/folders/18Tc4bz-KgPSqQnhc3MiK3vymABLoRflf?usp=sharing'").fetchone()[0]
    
    
    cursor = conn.cursor()
    for _, (asset_name, author, asset_packs, tags) in df_assets.iterrows():
        cursor.execute("insert into ASSET (name) values (?) RETURNING ASSET_ID", (asset_name,))
        asset_id = cursor.fetchone()[0]
        author_id = lk_authors[author]
        cursor.execute("insert into REL_ASSET_AUTHOR (ASSET_ID, AUTHOR_ID) values (?, ?)", (asset_id, author_id))
        asset_pack_ids = [(asset_id, lk_asset_packs[p]) for p in map(str.strip, asset_packs.split("|"))]
        cursor.executemany("insert into REL_ASSET_ASSET_PACK (ASSET_ID, ASSET_PACK_ID) values (?, ?)", asset_pack_ids)
        tag_ids = [(asset_id, lk_tags[t]) for t in map(str.strip, tags.split("|"))]
        cursor.executemany("insert into REL_TAG_ASSET (ASSET_ID, TAG_ID) values (?, ?)", tag_ids)
        cursor.executemany("insert into REL_ASSET_DOWNLOAD_LINK (ASSET_ID, DOWNLOAD_LINK_ID) values (?, ?)", [(asset_id, link_1_id), (asset_id, link_2_id)])
