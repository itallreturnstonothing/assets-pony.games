import sqlite3
import pandas as pd
import os

#%%

df_assets = pd.read_excel("assets.ods")

#%%

with sqlite3.connect("../test.sqlite3") as conn:
    conn.execute("PRAGMA foreign_keys=ON")
    cursor = conn.cursor()
    
    lk_tags = dict(cursor.execute("select name, TAG_ID from TAG").fetchall())
    lk_authors = dict(cursor.execute("select name, AUTHOR_ID from AUTHOR").fetchall())
    lk_asset_packs = dict(cursor.execute("select name, ASSET_PACK_ID from ASSET_PACK").fetchall())
    
    link_1_id = cursor.execute("select DOWNLOAD_LINK_ID from DOWNLOAD_LINK where url = 'https://mega.nz/folder/yKIGFSSS#148P2r8dwZlNSoCLVMKbKw'").fetchone()[0]
    link_2_id = cursor.execute("select DOWNLOAD_LINK_ID from DOWNLOAD_LINK where url = 'https://drive.google.com/drive/folders/18Tc4bz-KgPSqQnhc3MiK3vymABLoRflf?usp=sharing'").fetchone()[0]
    
    
    
    df_previews = df_assets["preview"].drop_duplicates().dropna().str.extract(r"(MARECON ASSET JAM(.*)/(.*)\.(.*))")[[0, 2, 3]]
    df_previews.columns = ["path", "filename", "extension"]
    df_previews["extension"] = df_previews["extension"].str.lower()
    
    if not os.path.exists("../asset_previews"):
        os.mkdir("../asset_previews")
    lk_previews = {}
    for _, (path, filename, extension) in df_previews.iterrows():
        cursor.execute("insert into PREVIEW (original_file_name, extension) values (?, ?) RETURNING PREVIEW_ID", (filename, extension))
        preview_id = cursor.fetchone()[0]
        lk_previews[path] = preview_id
        preview_path = f"../asset_previews/{preview_id}.{extension}"
        if not os.path.exists(preview_path):
            os.symlink(f"../marecon_asset_jam/{path}", preview_path)
    
    
    
    for _, (asset_name, author, asset_packs, tags, preview) in df_assets.iterrows():
        cursor.execute("insert into ASSET (name) values (?) RETURNING ASSET_ID", (asset_name,))
        asset_id = cursor.fetchone()[0]
        author_id = lk_authors[author]
        cursor.execute("insert into REL_ASSET_AUTHOR (ASSET_ID, AUTHOR_ID) values (?, ?)", (asset_id, author_id))
        if isinstance(preview, str):
            preview_id = lk_previews[preview]
            cursor.execute("insert into REL_ASSET_PREVIEW (ASSET_ID, PREVIEW_ID) values (?, ?)", (asset_id, preview_id))
        asset_pack_ids = [(asset_id, lk_asset_packs[p]) for p in map(str.strip, asset_packs.split("|"))]
        cursor.executemany("insert into REL_ASSET_ASSET_PACK (ASSET_ID, ASSET_PACK_ID) values (?, ?)", asset_pack_ids)
        tag_ids = [(asset_id, lk_tags[t]) for t in map(str.strip, tags.split("|"))]
        cursor.executemany("insert into REL_TAG_ASSET (ASSET_ID, TAG_ID) values (?, ?)", tag_ids)
        cursor.executemany("insert into REL_ASSET_DOWNLOAD_LINK (ASSET_ID, DOWNLOAD_LINK_ID) values (?, ?)", [(asset_id, link_1_id), (asset_id, link_2_id)])
