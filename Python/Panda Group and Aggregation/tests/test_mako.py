from ..functions import *
import os

columns = ["timestamp", "symbol", "volume", "price"]
csv_to_load = os.path.join(os.getcwd(), "tests/test_input.csv")
conn = sqlite3.connect(r'test.db')
db_table = 'daytradetest'


def test_load_csv():
    # check csv load works correctly
    df = load_csv_to_df(csv_to_load, columns)
    assert df.shape == (8, 4)


def test_aggregates():
    # check aggregates are correct according to precalculated values
    df = load_csv_to_df(csv_to_load, columns)
    df = prepare_dataframe(df)
    assert df.shape == (3, 4)
    result = [
        ["aaa", 5787, 40, 1161, 1222],
        ["aab", 6103, 69, 810, 907],
        ["aac", 3081, 41, 559, 638],
    ]
    r_columns = ['symbol', 'max_timegap', 'total_volume',
                 'weigthed_average_price', 'max_price']
    df2 = pd.DataFrame(result, columns=r_columns).set_index('symbol')
    assert df2.equals(df)


def test_save_db():
    # check loading to db and fetching is same as created result
    df = load_csv_to_df(csv_to_load, columns)
    df = prepare_dataframe(df)
    save_data_from_dataframe(df, db_table=db_table, conn=conn)
    df2 = pd.read_sql_query(f"SELECT * FROM {db_table}",
                            conn, index_col='symbol')
    assert df2.equals(df)


def test_max_10():
    # test that it returns max 10 ordered values
    result = [
        ["aab", 6103, 69, 810, 907],
        ["aab", 6103, 69, 810, 907],
        ["aab", 6103, 69, 810, 907],
        ["aab", 6103, 69, 810, 907],
        ["aac", 3081, 41, 559, 638],
        ["aaa", 5787, 40, 1161, 1222],
        ["aac", 3081, 41, 559, 638],
        ["aaa", 5787, 40, 1161, 1222],
        ["aac", 3081, 41, 559, 638],
        ["aaa", 5787, 40, 1161, 1222],
        ["aac", 3081, 41, 559, 638],
        ["aaa", 5787, 40, 1161, 1222],
        ["aac", 3081, 41, 559, 638],
        ["aaa", 5787, 40, 1161, 1222],
        ["aac", 3081, 41, 559, 638],
        ["aaa", 5787, 40, 1161, 1222],
    ]
    r_columns = ['symbol', 'max_timegap', 'total_volume',
                 'weigthed_average_price', 'max_price']
    df = pd.DataFrame(result, columns=r_columns).set_index('symbol')
    save_data_from_dataframe(df, db_table=db_table, conn=conn)
    df = fetch_10_biggest(db_table, conn)
    assert df.shape[0] <= 10
