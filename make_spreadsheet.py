import sqlite3
import pandas as pd

with open("format_like_google_sheet.sql") as query_fd:
    query = query_fd.read()

with sqlite3.connect("test.sqlite3") as conn:
    df_results = pd.read_sql(query, conn)

df_results.to_excel("asset_info.ods", index=False)