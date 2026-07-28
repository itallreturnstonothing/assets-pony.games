import sqlite3
import json

with sqlite3.connect("test.sqlite3") as conn, open("assets.json", "w") as outfile:
    cursor = conn.cursor()
    lk_tags = dict(cursor.execute("select TAG_ID, name from TAG").fetchall())
    lk_authors = dict(cursor.execute("select AUTHOR_ID, name from AUTHOR").fetchall())
    lk_asset_packs = dict(cursor.execute("select ASSET_PACK_ID, name from ASSET_PACK").fetchall())
    
    assets_result = cursor.execute("select ASSET_ID, name from ASSET").fetchall()
    
    assets = [{"id" : asset_id, "name" : name} for (asset_id, name) in assets_result]
    
    authors_result = cursor.execute("select ASSET_ID, AUTHOR_ID from REL_ASSET_AUTHOR").fetchall()
    tags_result = cursor.execute("select ASSET_ID, TAG_ID from REL_TAG_ASSET").fetchall()
    asset_packs_result = cursor.execute("select ASSET_ID, ASSET_PACK_ID from REL_ASSET_ASSET_PACK").fetchall()
    for asset in assets:
        asset_id = asset["id"]
        
        authors = [lk_authors[author_id] for (row_asset_id, author_id) in authors_result if row_asset_id == asset_id]
        asset["author"] = authors
        
        tags = [lk_tags[tag_id] for (row_asset_id, tag_id) in tags_result if row_asset_id == asset_id]
        asset["tags"] = tags
        
        packs = [lk_asset_packs[pack_id] for (row_asset_id, pack_id) in asset_packs_result if row_asset_id == asset_id]
        asset["asset_packs"] = packs
    
    json.dump(assets, outfile, indent=4)