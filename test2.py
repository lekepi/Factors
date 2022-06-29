import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':

    my_list = [[1, 'SPX', 1, 0.98], [2, 'SXXP', 2,  3.3]]
    df = pd.DataFrame(my_list, columns=['factor_id', 'index', 'quintile', 'value'])

    print(df)
