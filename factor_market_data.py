import pandas as pd
from models import session, Factor, FactorMarketData
from datetime import date
import numpy as np


def calc_normalize(my_serie, factor):
    norm_calculation = factor.norm_calculation
    if norm_calculation == 'same':  # No Change - already normalized
        return my_serie

    temp_serie = my_serie
    if factor.min_value:
        temp_serie = temp_serie.where(temp_serie >= factor.min_value, factor.min_value)
    if factor.max_value:
        temp_serie = temp_serie.where(temp_serie <= factor.max_value, factor.max_value)

    if norm_calculation == 'log_norm':  # calculate the log
        min_value = temp_serie.min()
        temp_serie = (temp_serie + 1 - min_value).apply(np.log)
    elif norm_calculation == 'sqrt_norm':  # calculate the sqrt
        temp_serie = temp_serie.pow(0.5)  #  temp_serie.apply(np.sqrt())

    # Standardize and Winsorize
    temp_serie = (temp_serie - temp_serie.mean()) / temp_serie.std()
    temp_serie = temp_serie.where(temp_serie <= 3, 3)
    temp_serie = temp_serie.where(temp_serie >= -3, -3)

    return temp_serie


def download_factor_market_data(my_date):

    session.query(FactorMarketData).filter(FactorMarketData.entry_date == my_date).delete()
    session.commit()

    indexes = ['SPX', 'SXXP']
    factors = session.query(Factor).all()

    my_date_str = my_date.strftime("%Y-%m-%d")
    file_path = fr"\\ANLDFS\users$\Olivier\Factors\Key Files\Factor Market Data - {my_date_str}.xlsm"

    factor_md_list = []
    factor_quintile = []

    for index in indexes:
        for factor in factors:
            sheet_name = f"{index}-{factor.short_name}"
            factor_id = factor.id
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            df['norm'] = calc_normalize(df['Value'], factor)

            for i in range(1, 6):
                quintile_value = df.loc[df['Quintile'] == i, 'norm'].mean()  # TODO calculate
                factor_quintile.append([factor.id, index, i, quintile_value])

            for i, row in df.iterrows():
                ticker = row['Ticker']
                raw_value = row['Value']
                linear_value = row['Coeff']
                norm_value = row['norm']
                quintile = row['Quintile']

                new_factor_md = FactorMarketData(entry_date=my_date,
                                                 ticker=ticker,
                                                 factor_id=factor_id,
                                                 index=index,
                                                 raw_value=raw_value,
                                                 linear_value=linear_value,
                                                 norm_value=norm_value,
                                                 quintile=quintile)
                factor_md_list.append(new_factor_md)
            print(sheet_name)

    df_missing = pd.read_excel(file_path, sheet_name='FTW Security', usecols="J:O")
    df_missing = df_missing.dropna()

    df_quintile = pd.DataFrame(factor_quintile, columns=['factor_id', 'index', 'quintile', 'value'])

    for index, row in df_missing.iterrows():

        factor_id = row['Factor_id']
        my_index = row['Index']
        quintile = row['Quintile']
        linear_value = row['Coeff']
        ticker = row['Ticker']

        norm_value = df_quintile[(df_quintile['index'] == my_index) &
                                 (df_quintile['quintile'] == quintile) &
                                 (df_quintile['factor_id'] == factor_id)]['value'].values[0]

        new_factor_md = FactorMarketData(entry_date=my_date,
                                         ticker=ticker,
                                         factor_id=factor_id,
                                         linear_value=linear_value,
                                         norm_value=norm_value,
                                         index=my_index,
                                         quintile=quintile)
        factor_md_list.append(new_factor_md)

    session.add_all(factor_md_list)
    session.commit()

    print('Done')


if __name__ == "__main__":
    my_date = date.today()
    # my_date = date(2022, 6, 24)
    my_date = date(2022, 7, 15)
    download_factor_market_data(my_date)
