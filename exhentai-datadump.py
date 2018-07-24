import requests
import re
import json
import uuid
import glob
import sqlite3
import time
from bypy import ByPy
from bs4 import BeautifulSoup
cookd = {
	"igneous": "89540adbd",
    "ipb_member_id": "2237746",
    "ipb_pass_hash": "d99e752060d5e11636d7e427f62a3622",
    "lv": "1532257034-1532318327"
}
excook = requests.utils.cookiejar_from_dict(cookd, cookiejar=None, overwrite=True)
exhead = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
    "Connection": "keep-alive",
    "Host": "exhentai.org",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}
hlist = []
eoltoken = "null"
merge = []
hlistc = 0
for pgn in range(0, 500):
	exurl =  "https://exhentai.org/?page="+ str(pgn)+ "&f_doujinshi=1&f_manga=1&f_artistcg=1&f_gamecg=1&f_western=1&f_non-h=1&f_imageset=1&f_cosplay=1&f_asianporn=1&f_misc=1&f_search=&f_apply=Apply+Filter&advsearch=1&f_sname=on&f_stags=on&f_sh=on&f_srdd=2"
	orig = requests.get(exurl, headers=exhead, cookies=excook).text
	if "No hits found" in orig:
		break
	else:
		BSorig = BeautifulSoup(orig)
	table = BSorig.find("table", {"class": "itg"})
	for link in table.findAll("a", href=re.compile("https://exhentai\.org/g/[0-9]{1,8}/[A-Za-z0-9]{10}/")):
		if "href" in link.attrs:
			link2 = link.attrs["href"]
			hlist.append(link2.split("/")[4:6])
	if eoltoken in hlist:
		eol = hlist.index(eoltoken)
		hlist = hlist[eol+1:len(hlist)]
	eollist = hlist[-1]
	print(hlist)
	req = {
		"method": "gdata",
		"gidlist": hlist,
		"namespace": 1
	}
	recl = json.loads(json.dumps(requests.post("https://api.e-hentai.org/api.php", data=json.dumps(req, ensure_ascii=False).encode("utf-8")).json(), ensure_ascii=False), encoding="UTF-8")['gmetadata']
	for obj in recl:
		with open(str(uuid.uuid4())+".json", "w", encoding="UTF-8") as f:
			json.dump(obj, f, ensure_ascii=False)
	hlistc = hlistc + 1
	if hlistc >4:
		time.sleep(5)
		hlistc = 0
	hlist.clear()		
for f in glob.glob("*.json"):
	with open(f, "rb") as inf:
		merge.append(json.load(inf))
with open("fin.json", "w", encoding="UTF-8") as out:
	json.dump(merge, out, ensure_ascii=False, sort_keys=True)
ByPy().quota()
ByPy().upload("fin.json", "fin.json", "overwrite")
