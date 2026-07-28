with
tags_for_asset as (
    select group_concat(TAG.name, ', ') as tags, ASSET.ASSET_ID
    from REL_TAG_ASSET as rel
        join TAG on rel.TAG_ID = TAG.TAG_ID
        join ASSET on rel.ASSET_ID = ASSET.ASSET_ID
    group by ASSET.ASSET_ID
),
asset_packs_for_asset as (
    select group_concat(PACK.name, '/') as asset_packs, ASSET.ASSET_ID
    from REL_ASSET_ASSET_PACK as rel
        join ASSET_PACK as PACK on rel.ASSET_PACK_ID = PACK.ASSET_PACK_ID
        join ASSET on rel.ASSET_ID = ASSET.ASSET_ID
    group by ASSET.ASSET_ID
),
authors_for_asset as (
    select group_concat(AUTHOR.name, ', ') as author, ASSET.ASSET_ID
    from REL_ASSET_AUTHOR as rel
        join AUTHOR on rel.AUTHOR_ID = AUTHOR.AUTHOR_ID
        join ASSET on rel.ASSET_ID = ASSET.ASSET_ID
    group by ASSET.ASSET_ID
)

select name, author, asset_packs, tags from ASSET natural join tags_for_asset natural join asset_packs_for_asset natural join authors_for_asset;
