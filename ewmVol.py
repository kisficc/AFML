import datetime
import pandas as pd
import pymysql
from sqlalchemy import create_engine
# MySQL Connector using pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

################################################################################
##  Database
################################################################################
# Connect to the database - nubes_test
print('Connecting to the database...\n')
engine_mysql_nubes_test = create_engine(
    'mysql+mysqldb://%s:%s@%s/%s' % (
        'ki_user2',         # ID
        'gksxnAI@2',        # Password
        '192.168.195.23',   # IP Address, port 3306
        'nubes_test'),      # Schema
    encoding = 'utf-8')
conn_nubes_test = engine_mysql_nubes_test.connect()

# Tables - nubes_test
mysql_table_stock_price_data = 'y_stock_price_data'

# Get the historical price
hist_price_005930 = pd.read_sql_query(
    "SELECT * from " + mysql_table_stock_price_data 
    + " WHERE code = '005930 KS Equity'", 
    conn_nubes_test)

hist_price_005930_df = pd.DataFrame(
    data=hist_price_005930['price'].values,
    index=hist_price_005930['date'].values,
    columns=['005930 KS Equity'], 
    dtype=None)
hist_price_005930_df.index = pd.to_datetime(
    hist_price_005930_df.index, 
    format = '%Y-%m-%d')
close = close['005930 KS Equity'].values

def getDailyVol(close, span0=100):
    # Daily Vol. reindexed to close
    df0 = close.index.searchsorted(close.index - pd.Timedelta(days=1))
    df0 = df0[df0>0]
    df0 = pd.Series(
        close.index[df0-1], 
        index=close.index[close.shape[0]-df0.shape[0]:])
    df0 = close.loc[df0.index] / close.loc[df0.values].values - 1 # daily returns
    df0 = df0.ewm(span = span0).std()
    return df0
