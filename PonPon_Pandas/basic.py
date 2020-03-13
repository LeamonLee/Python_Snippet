import pandas as pd

# 建立 Series
data = pd.Series([20,15,10])

# 基本 Series操作
print(data)
print()

print("Max: ", data.max())
print("Min: ", data.min())
print("Median: ", data.median())
print()

data = data * 2
print(data)
print()

data = data == 20
print(data)
print()


# 建立 DataFrame
dataFrame = pd.DataFrame({
    "name": ["Amy", "John", "Bob"],
    "salary": [30000, 40000, 50000]
})

# 基本 DataFrame操作
print(dataFrame)
print()

# 取得特定的欄位
print(dataFrame["name"])
print()

# 取得特定的列
print(dataFrame.iloc[0])        # 取得第1列的資料     
print()                                 



