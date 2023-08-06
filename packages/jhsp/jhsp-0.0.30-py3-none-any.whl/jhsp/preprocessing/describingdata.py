import pandas as pd
import os


class DescribingData:
    def __init__(self, old_dir):
        self.data = self.data = pd.read_excel(old_dir, header=0)  # 第一行默认为表头，数据第一行必须有表头
        self.save_dir = os.path.dirname(old_dir)

    def to_medical_his(self):
        data = self.data.copy()
        save_path = os.path.join(self.save_dir, 'medical_history.xlsx')

        for column in list(data.columns.values):
            if {0,1} == set(data.loc[:,column].tolist()):
                data.loc[data[column]==1,[column]] = column

        data.to_excel(save_path)

