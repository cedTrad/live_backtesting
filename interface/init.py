
import pandas as pd
import sqlalchemy

def Data(table):
    path = "C:/Users/cc/Desktop/CedAlgo/Bot_v_5/data/trade/"
    engine = sqlalchemy.create_engine(f'sqlite:///'+path+'BTCUSDT_LS.db')
    data = pd.read_sql(table, engine)
    return data

def merge(table1, table2):
    if isinstance(table1, str) and isinstance(table2, str):
        data = Data(table1).merge(Data(table2), on = "identifier")
        data.drop(columns = ["date_y", "trade_id_y"], inplace = True)
        data.rename(columns = {"date_x" : "date", "trade_id_x" : "trade_id"}, inplace = True)
        return data
    else:
        raise("Type Error")
    
