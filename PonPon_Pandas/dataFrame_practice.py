import pandas as pd

# 建立自訂索引的資料
dataFrame = pd.DataFrame({
    "name":["Amy", "Bob", "Charles"],
    "salary":[30000, 40000, 50000]
}, index=['a', 'b', 'c'])
print(dataFrame)
print()

print("size: ", dataFrame.size)         # 印出size屬性，一個格子就是1筆資料，所以如果是2*3的資料，總共就有6筆
print("shape(row, column): ", dataFrame.shape)     # 印出shape屬性
print("index: ", dataFrame.index)       # 印出index屬性
print()

# 取得列(row)的資料
print("取得第二列: ", dataFrame.iloc[1], sep="\n")      # 根據順序
print("取得第二列: ", dataFrame.loc['b'], sep="\n")      # 根據索引
print()

# 取得欄(column)的資料
print("取得 name 欄位: ", dataFrame["name"], sep="\n")          # 根據欄位名稱 dataFrame[欄位名稱]

names = dataFrame["name"]                               # dataFrame取得一個row或一個column的資料後，會變成Series型態(單維度資料)
print("把 names 全部轉成大寫", names.str.upper(), sep="\n")

salaries = dataFrame["salary"]
print("計算薪水的平均值: ", salaries.mean())
print()

# 建立新的欄位
dataFrame["revenue"] = [500000, 400000, 300000]                         # dataFrame[新欄位名稱] = 列表
dataFrame["rank"] = pd.Series([3,6,1], index=['a', 'b', 'c'])           # dataFrame[新欄位名稱] = Series資料
dataFrame["cp"] = dataFrame["revenue"] / dataFrame["salary"]               # 根據現有欄位, 創造新欄位
print(dataFrame)
print()