import pandas as pd
import urllib.request
import zipfile
import statsmodels.api as sm


def get_alto_ftw_reg():
    df = pd.read_excel("H:\\Factors\\FTW Regression 2024-10-30.xlsx", sheet_name='Summary')
    df.drop(columns=['Date'], inplace=True)
    # print(df.dtypes)
    y = df['Alto']

    #X all columns except last
    col_list = df.columns.tolist()
    X = df[col_list[:-1]]
    X_sm = sm.add_constant(X)

    model = sm.OLS(y, X_sm)
    results = model.fit()

    print(results.summary())

    coefficients = results.params.round(5)
    print(coefficients)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_alto_ftw_reg()





