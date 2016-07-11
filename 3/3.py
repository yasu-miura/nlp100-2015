# coding:utf-8
import json
import re
from collections import Counter
import requests


# 20.JSONデータの読み込み
with open("./jawiki-country.json", "r") as f:
    line = f.readline()
    while line:
        wiki = json.loads(f.readline())
        if wiki["title"] == u"イギリス":
            line = None

# 21. カテゴリ名を含む行を抽出
pattern = re.compile("\[\[Category:.*\]\]\n")
cat_list = pattern.findall(wiki["text"])

# 22.カテゴリ名の抽出
pattern = re.compile(":.*\||:.*\]")
cname_list = []
for cat in cat_list:
    m = pattern.search(cat)
    cname = cat[m.span()[0]+1: m.span()[1]-1].replace("]", "")
    cname_list.append(cname)

# 23.セクション構造
pattern = re.compile("=[=]+.*=[=]+\n")
sec_list = pattern.findall(wiki["text"])
print("~~~~~~~~~~~~セクション構造~~~~~~~~~~~~")
for sec in sec_list:
    c = Counter(sec)
    print sec.replace("=", "").replace("\n", "") + ":" + str((c["="] / 2) - 1)

# 24.ファイル参照の抽出
'''
=http://~ .htm or .html|
File:Elizaq ~ .jpg png| etc.....
ファイル; ~ .jpg|
<ref>[http://www.sh.xinhuanet.com/shstatics/images2013/IFCD2013_En.pdf Xinhua-Dow Jones International Financial Centers Development Index （2013)] (2013年9月公表)</ref>
'''
url = "https?://[-_.!~*\'();\/?:@&+=\$,%#a-zA-Z0-9]*[\s\|]{1}"
file_pattern = u"File:[a-zA-Z0-9\s]+\.[a-z]+\||ファイル:[a-zA-Z0-9\s]+\.[a-z]+\|"
pattern = re.compile(url + "|" + file_pattern)
medias = pattern.findall(wiki["text"])
media_list = []
for media in medias:
    if media.startswith(u"ファイル") or media.startswith(u"File"):
        media = media[5:len(media)-1]
        media_list.append(media)
    elif media.startswith(u"http"):
        if media[-1] == "|":
            media_list.append(media[0:len(media)-1])
        else:
            media_list.append(media)


# 25.テンプレートの抽出
lines = wiki["text"].split("\n")
index = 0
infos = {}
rm_pattern = r"<ref.*/>|<ref.*</ref>"
line = lines[index]
while line:
    line = lines[index]
    if line.startswith("}}"):
        line = None
    elif line.startswith("|"):
        key, value = line[1:len(line)].split(" = ")
        infos[key] = re.sub(rm_pattern, "", value)
    index += 1


# 26.強調マークアップの除去&27.内部リンクの除去&28.MediaWikiマークアップの除去
def replace_markup(text):
    # 強調の除去
    em_pattern = r"'''''|'''|''"
    text = re.sub(em_pattern, "", text)
    markup_pattern = re.compile("\[\[.*?\]\]|\{\{.*?\}\}")
    match_list = markup_pattern.findall(text)
    cleaned_list = []
    for match in match_list:
        sep = match.split("|")
        # [[ロンドン]]
        if len(sep) == 1:
            cleaned_text = sep[0][2:len(sep[0])-2]
        # [[連合法 (1707年)|1707年連合法]]
        elif len(sep) == 2:
            cleaned_text = sep[0][2:]
        elif len(sep) == 3:
            # {{lang|en|United Kingdom of Great Britain and Northern Ireland}}
            if sep[0].startswith("{"):
                cleaned_text = sep[2][:len(sep[2])-2]
            # [[ファイル:Royal Coat of Arms of the United Kingdom.svg|85px|イギリスの国章]]
            elif sep[0].startswith("["):
                cleaned_text = sep[0][7:]
        cleaned_list.append(cleaned_text)
    for index in range(len(match_list)):
        text = text.replace(match_list[index], cleaned_list[index])
    return text

for key in infos:
    print key + ":" + replace_markup(infos[key])

# 29.国旗画像のURLを取得する
# 画像を取得するwikiのWebAPIいけてねぇな・・・
payload = {"action": "query", "prop": "imageinfo", "iiprop": "url", "format": "json", "titles": "File:" + infos[u"国旗画像"]}
response = requests.get("https://commons.wikimedia.org/w/api.php", params=payload)
result = json.loads(response.text)
print result["query"]["pages"]["347935"]["imageinfo"][0]["url"]
