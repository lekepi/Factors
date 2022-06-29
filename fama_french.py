import pandas as pd
import urllib.request
import zipfile
import statsmodels.api as sm


def fama_french_reg(my_type):

    alto_perf = pd.read_csv("H:\\Factors\\Fama French Data\\Python\\alto perf.csv", parse_dates=['Date'])
    if my_type == 'US_3F':
        ff_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip"
        csv_name = 'F-F_Research_Data_Factors.csv'
        col_list = ['Date', 'Mkt-RF', 'SMB', 'HML', 'RF']
    elif my_type == 'Dev_3F':
        ff_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_3_Factors_CSV.zip"
        csv_name = 'Developed_3_Factors.csv'
        col_list = ['Date', 'Mkt-RF', 'SMB', 'HML', 'RF']
    elif my_type == 'Dev_5F':
        ff_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_5_Factors_CSV.zip"
        csv_name = 'Developed_5_Factors.csv'
        col_list = ['Date', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'RF']

    urllib.request.urlretrieve(ff_url, 'fama_french.zip')
    zip_file = zipfile.ZipFile('fama_french.zip', 'r')
    zip_file.extractall()
    zip_file.close()
    ff_factors = pd.read_csv(csv_name, skiprows=3)

    ff_factors.columns = col_list

    ff_factors.dropna(axis='index', how='any', subset=['Date'], inplace=True)
    index = ff_factors.loc[ff_factors['Date'].str.contains('Annual Factors: January-December')].index[0]
    ff_factors = ff_factors.iloc[:index]
    ff_factors['Date'] = ff_factors['Date'].str.strip() + "01"
    ff_factors['Date'] = pd.to_datetime(ff_factors['Date'], format='%Y%m%d')
    ff_factors[col_list[1:]] = ff_factors[col_list[1:]].apply(pd.to_numeric) / 100
    df = pd.merge(ff_factors, alto_perf)

    # print(df.dtypes)
    y = df['return-RF']
    X = df[col_list[1:-1]]
    X_sm = sm.add_constant(X)

    model = sm.OLS(y, X_sm)
    results = model.fit()

    print(results.summary())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fama_french_reg('US_3F')  # US Market, 3 Factors
    fama_french_reg('Dev_3F')  # Developed country, 3 Factors
    fama_french_reg('Dev_5F')  # Developed country, 3 Factors





