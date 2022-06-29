from datetime import date
import pandas as pd
from models import session, engine, FactorMarketData, Factor
import matplotlib.pyplot as plt
import csv


def display_data(my_date):
    my_sql = f"""SELECT short_name as factor,ticker,T1.index,value FROM factor_market_data T1 JOIN factor T2
ON T1.factor_id=T2.id  WHERE entry_date='{my_date}' order by short_name;"""

    df = pd.read_sql(my_sql, engine)
    factor_list = session.query(Factor).all()

    for factor in factor_list:
        df_factor = df[df['factor'] == factor.short_name]
        df_factor = df_factor.dropna()
        num_list = df_factor['value'].tolist()
        plt.hist(num_list, bins=20)
        plt.title(factor.short_name)
        plt.show()


if __name__ == '__main__':
    my_date = date(2022, 6, 24)
    display_data(my_date)
