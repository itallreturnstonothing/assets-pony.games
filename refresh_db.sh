DBNAME='test.sqlite3'
sqlite3 $DBNAME < schema.sql
cat tags.sql authors.sql asset_packs.sql | sqlite3 $DBNAME
