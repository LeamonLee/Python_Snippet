import pandas as pd

# 建立自訂索引的資料
dataSeries = pd.Series([4,5,-2,3,7], index=['a', 'b', 'c', 'd', 'e'])
print(dataSeries)
print()

print("dtype: ", dataSeries.dtype)  # 印出 dtype 屬性
print("size: ", dataSeries.size)    # 印出 size 屬性
print("index: ", dataSeries.index)  # 印出 index 屬性
print()

# 取得資料: 根據順序, 根據索引
print(dataSeries[2])                # 根據順序 取得第2筆資料
print(dataSeries['c'])              # 根據索引 取得第2筆資料
print()

# 數字運算: 基本, 統計, 順序
print("min, max, sum:", dataSeries.min(), dataSeries.max(), dataSeries.sum())
print("mean, median, std:", dataSeries.mean(), dataSeries.median(), dataSeries.std())
print("nlargest: ", dataSeries.nlargest(3))              # 取得前3大
print("nsmallest:", dataSeries.nsmallest(2))           # 取得前2小
print()

# 字串運算: 基本, 串接, 搜尋, 取代
dataSeries2 = pd.Series(["您好", "Python", "Pandas"])
print(dataSeries2.str.lower())
print(dataSeries2.str.len())
print(dataSeries2.str.cat(sep=','))             # 把字串串起來, 中間用,隔開
print(dataSeries2.str.contains('P'))            # 判斷是否包含大寫P
print(dataSeries2.str.replace("您好", "Hello"))    



