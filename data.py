%matplotlib inline

import datetime

import pandas as pd
from pandas import to_datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from scipy.interpolate import make_interp_spline



register_matplotlib_converters()

file_path = "D://test_data/.btctradeCNY.csv"
# 读取整个csv文件,并增加标题列
csv_data = pd.read_csv(file_path,names=["time_stamp","price","trade"],float_precision='round_trip',encoding='utf8')

# 去掉数据重复的行
csv_data = csv_data.drop_duplicates()

# 去掉价格为0的数据
csv_data=csv_data[csv_data['price']!=0]

# 将时间戳转为日期
csv_data['date']=pd.to_datetime(csv_data['time_stamp'],unit='s',origin=pd.Timestamp('1970-01-01'))

# 增加一列当前日期的当前行交易总价row_total_price(price*trade)
# note.暂时不考虑price与trade列值存在为空的情况(否则合并结果为空，需做NA处理，替换或者删除)
csv_data['row_total_price']=csv_data['price']*csv_data['trade']

# 按年-月进行分组聚合
csv_data=csv_data.set_index('date') # 重置索引
key=lambda date:(date.year,date.month)
group = csv_data['row_total_price'].groupby(key)

# 获取最大的交易量月份
data_info = group.sum().to_dict()
max_transaction_month_tuple = max(data_info, key=data_info.get)
transaction_price = data_info.get(max_transaction_month_tuple)
max_transaction_month = '-'.join(str(i) for i in max_transaction_month_tuple)
print(f"最大成交量月份:{max_transaction_month}，当月成交总价:{transaction_price:0,.5f}")

#  根据最大成交量月份:max_transaction_month，获取指定月份的数据
max_month_result_data = csv_data[max_transaction_month]
print (max_month_result_data)

# 再次按年-月-日聚合数据
key=lambda date:(date.year,date.month,date.day)
group = max_month_result_data['row_total_price'].groupby(key)
result_data = group.sum().to_dict()

# 根据交易量最大月份result_data的日期进行绘制曲线图
x,y=[],[]
for date_tuple,total_price_by_day in result_data.items():
    x.append(datetime.date(*date_tuple))
    y.append(total_price_by_day)

plt.plot(x,y,linewidth=1,markersize=12,label="First")
plt.xticks(x,rotation=90)#设置时间标签显示格式
plt.figure()# 创建画布
plt.show()


# # 将处理后的数据写入新的csv文件
# csv_data.drop("time_stamp",axis=1,inplace=True)  
# csv_data.to_csv("D://test_data/new_data.csv")      

