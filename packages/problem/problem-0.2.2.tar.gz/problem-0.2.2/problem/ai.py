import pandas as pd
import numpy as np
from IPython.display import clear_output
from sklearn.model_selection import train_test_split

class preprocessing:
    def onehot_weekday_maker(self, df):
        df_dayName = pd.DataFrame({'weekday':df.index.day_name()})
        return pd.get_dummies(df_dayName.weekday).reindex(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']).fillna(0)

    def train_test_validation_split(self, _x, _y, train_size=0.7, validation_size=0.1, test_size=0.2, shuffle=False):
        #X_train, X_validation, X_test, Y_train, Y_validation, Y_test = train_test_validation_split(X, Y, shuffle=False)
        x, x_test, y, y_test = train_test_split(_x, _y, train_size=train_size+validation_size, test_size=test_size, shuffle=shuffle)
        x_train, x_validation, y_train, y_validation = train_test_split(x, y, train_size=(train_size/(train_size+validation_size)), shuffle=shuffle)
        return x_train, x_validation, x_test, y_train, y_validation, y_test


def clear_print():
    clear_output()