import re

str1: str
str2: str

str1 = "/NOT_SYNC 49/tagoken-shared/movies/2018-07-20/00273.MTS"
str1 = "/NOT_SYNC 6/tagoken-shared/movies/2015-02-02/.DS_Store"
print(re.match('/[^/]+/(.+)', str1).groups())
str2 = re.match('/[^/]+/(.+)', str1).group(1)

print("正規表現前： " + str1)
print("正規表現後： " + str2)
