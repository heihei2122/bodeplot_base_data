import pandas as pd
import numpy as np
import csv
#创建包含时间序列的数据
with open("Scope Project.csv",errors='ignore') as f:
    f_csv=csv.reader(f)
    for row in f_csv:
        if row:
            data=row[0].split('\t')
        
