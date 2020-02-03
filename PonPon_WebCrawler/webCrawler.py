import urllib.request as req
import bs4


strUrl = "https://www.ptt.cc/bbs/movie/index8620.html"

# 建立一個Request物件, 附加Request Headers資訊 來模仿一個正常人使用瀏覽器的情況
request = req.Request(strUrl, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
})

# with req.urlopen(strUrl) as response:
with req.urlopen(request) as response:
    data = response.read().decode("utf-8")

print(data)

# 解析原始碼, 取得每篇文章的標題
root = bs4.BeautifulSoup(data, "html.parser")
# print(root.title)
# print(root.title.string)

# title = root.find("div", class_="title")     # 尋找一個 class="title"的div標籤
titles = root.find_all("div", class_="title")   # 尋找所有 class="title"的div標籤
# print(title)
# print(title.a.string)

for title in titles:
    # 如果標題有a標籤才印出來
    if title.a != None:
        print(title.a.string)

