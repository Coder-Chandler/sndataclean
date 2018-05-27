import time
import pandas as pd



excel_path = '/Users/chandler/Documents/Projects/sndataclean/524_leiji/5.1-5.24_output.xlsx'
# 读取文件路径至pandas转换为dataframe
read_df = pd.read_excel(excel_path, sheetname='leiji')
print(read_df)



