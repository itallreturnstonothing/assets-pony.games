DBNAME='test.sqlite3'
sqlite3 $DBNAME < schema.sql
cat tags.sql authors.sql asset_packs.sql download_links.sql | sqlite3 $DBNAME
