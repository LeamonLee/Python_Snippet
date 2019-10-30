# import urllib

# data = {'username':'administrator', 'password':'xyz'}
# result = urllib.parse.urlencode(data)
# print(result)


# =================================================================

from urllib.parse import urlencode, quote, unquote,quote_plus

payload = {'username':'administrator', 'password':'xyz'}
# result = urlencode(payload, quote_via=quote_plus)
result = urlencode(payload)
print(result)

result = quote("哈囉")
print("quote() :", result)

result = unquote(result)
print("unquote() :", result)
