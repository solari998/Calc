from datetime import datetime, timedelta
from calendar import monthrange

import pandas as pd
import numpy as np


class BasisRisk(object):
    start_date = datetime(2005, 1, 1)
    end_date = datetime(2017, 1, 1)
    interval = timedelta(days=90)

    def __init__(self) -> None:
        super().__init__()
        self.curves = None

    def input_data(self):
        self.curves = pd.read_excel("curve.xls")

    def preprocessing(self):
        self.curves['basis5y'] = self.curves.loan5y - self.curves.cdb5y
        self.curves['basis10y'] = self.curves.loan5y - self.curves.cdb10y

        ma_list = [30, 92, 183, 365, 365 * 5]

        for ma in ma_list:
            self.curves["cdb5y_ma" + str(ma)] = pd.rolling_mean(self.curves.cdb5y, ma)
            self.curves["cdb10y_ma" + str(ma)] = pd.rolling_mean(self.curves.cdb10y, ma)
            self.curves['basis5y_ma' + str(ma)] = self.curves.loan5y - self.curves["cdb5y_ma" + str(ma)]
            self.curves['basis10y_ma' + str(ma)] = self.curves.loan5y - self.curves["cdb10y_ma" + str(ma)]

        self.curves.to_csv("1.csv")

    def select(self):
        curves = self.curves
        intervals = (self.end_date - self.start_date).days // self.interval.days

        df = pd.DataFrame()

        for i in range(intervals):
            new_date = self.start_date + timedelta(days=i * 90)
            value = curves.loc[curves.date == new_date]
            df = df.append(value)

        print(df.mean())


if __name__ == "__main__":
    br = BasisRisk()
    br.input_data()
    br.select()
    print(br.curves.head())
