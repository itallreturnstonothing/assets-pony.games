import sqlite3
import json

with sqlite3.connect("test.sqlite3") as conn, open("resources.json", "w") as outfile:
    cursor = conn.cursor()
    lk_tags = dict(cursor.execute("select TAG_ID, name from TAG").fetchall())
    lk_authors = dict(cursor.execute("select AUTHOR_ID, name from AUTHOR").fetchall())
    lk_asset_packs = dict(cursor.execute("select ASSET_PACK_ID, name from ASSET_PACK").fetchall())
    lk_download_links = dict(cursor.execute("select DOWNLOAD_LINK_ID, url from DOWNLOAD_LINK").fetchall())
    lk_previews = dict(cursor.execute("select PREVIEW_ID, unique_file_name from PREVIEW").fetchall())
    
    assets_result = cursor.execute("select ASSET_ID, name, description from ASSET").fetchall()
    
    assets = [{
        "id" : asset_id,
        "name" : name,
        "description" : description if description else ""
    } for (asset_id, name, description) in assets_result]
    
    authors_result = cursor.execute("select ASSET_ID, AUTHOR_ID from REL_ASSET_AUTHOR").fetchall()
    tags_result = cursor.execute("select ASSET_ID, TAG_ID from REL_TAG_ASSET").fetchall()
    asset_packs_result = cursor.execute("select ASSET_ID, ASSET_PACK_ID from REL_ASSET_ASSET_PACK").fetchall()
    download_links_result = cursor.execute("select ASSET_ID, DOWNLOAD_LINK_ID from REL_ASSET_DOWNLOAD_LINK").fetchall()
    previews_result = cursor.execute("select ASSET_ID, PREVIEW_ID from REL_ASSET_PREVIEW").fetchall()
    for asset in assets:
        asset_id = asset["id"]
        
        authors = [lk_authors[author_id] for (row_asset_id, author_id) in authors_result if row_asset_id == asset_id]
        asset["author"] = authors
        
        tags = [lk_tags[tag_id] for (row_asset_id, tag_id) in tags_result if row_asset_id == asset_id]
        asset["tags"] = tags
        
        packs = [lk_asset_packs[pack_id] for (row_asset_id, pack_id) in asset_packs_result if row_asset_id == asset_id]
        asset["assetPacks"] = packs
        
        links = [lk_download_links[link_id] for (row_asset_id, link_id) in download_links_result if row_asset_id == asset_id]
        asset["downloads"] = links
        
        previews = ["/asset_previews/" + lk_previews[preview_id] for (row_asset_id, preview_id) in previews_result if row_asset_id == asset_id]
        asset["previews"] = previews
        
        asset["thumbnail"] = previews[0] if previews else "/asset_previews/generic.png"
        
        
    resources = {
        "allTags" : list(lk_tags.values()),
        "allAuthors" : list(lk_authors.values()),
        "allAssetPacks" : list(lk_asset_packs.values()),
        "assets" : assets
    }
    
    json.dump(resources, outfile, indent=4)
