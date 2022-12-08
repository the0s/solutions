# load required libraries
import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect(r'database.db')
db_table = 'daytrade'
csv_to_load = 'input.csv'
columns = ["timestamp", "symbol", "volume", "price"]


def load_csv_to_df(csv_to_load, columns=columns):
    return pd.read_csv(csv_to_load, names=columns)


def prepare_dataframe(df_main):
    # Convert to specific types
    df_main[["volume", "price", "timestamp"]] = df_main[[
        "volume", "price", "timestamp"]].apply(pd.to_numeric)
    df_main[["symbol"]] = df_main[["symbol"]].astype(str)

    # sort, find differences per group and create new column
    df = df_main[["timestamp", "symbol"]].sort_values(
        'timestamp', ascending=True)
    df_main['timegap'] = df.groupby('symbol').diff()

    # create a function to find weigthed from dataframe
    weighted_fn = lambda x: np.average(
        x, weights=df_main.loc[x.index, "volume"])

    # Create aggregates
    df_result = df_main.groupby(["symbol"]).agg(
        max_timegap=("timegap", 'max'),
        total_volume=("volume", "sum"),
        weigthed_average_price=(
            "price", weighted_fn),
        max_price=("price", "max"),
    )
    df_result[["weigthed_average_price", "max_timegap"]] = df_result[[
        "weigthed_average_price", "max_timegap"]].astype(int)

    return df_result


def save_data_from_dataframe(df_result, db_table=db_table, conn=conn):
    # create table and add data
    df_result.to_sql(db_table, conn, if_exists='replace')


def fetch_10_biggest(db_table, conn):
    # Fetch 10 biggest symbols by total volume of this day
    query = '''SELECT * FROM {db_table}
            ORDER BY total_volume DESC
            LIMIT 10
            '''.format(db_table=db_table)
    return pd.read_sql_query(query, conn, index_col='symbol')


if __name__ == "__main__":
    conn = sqlite3.connect(r'database.db')
    df = load_csv_to_df(csv_to_load, columns)
    df = prepare_dataframe(df)
    save_data_from_dataframe(df, db_table, conn)
    df = fetch_10_biggest(db_table, conn)
    print(df)

