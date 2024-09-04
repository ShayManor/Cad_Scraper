import json

with open('../Data/content.json') as f:
    urls = json.load(f)
for url in urls:
    while urls.count(url) > 1:
        urls.remove(url)
print(urls)
print(len(urls))