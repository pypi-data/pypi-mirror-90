import urllib.request
#from xes.common import  *
class LoadWork:
    def __init__(self,pid):
        self.pid=pid
    def get_likes(self):
        try:
            url="http://code.xueersi.com/api/compilers/"+str(self.pid)+"?id="+str(self.pid)
            headers = {'Content-Type':'application/json'}
            a=requests.get(url=url, headers=headers)
            null,false,list_get,string=0,0,[],''
            p=json.loads(a.text)
            likes=p["data"]["likes"]
            return likes
        except:
            return -1
    def get_user(self):
        try:
            url = "http://code.xueersi.com/api/compilers/" + str(self.pid) + "?id=" + str(self.pid)
            print(url)
            headers = {'Content-Type': 'application/json'}
            a = requests.get(url=url, headers=headers)
            null, false, list_get, string = 0, 0, [], ''
            p = json.loads(a.text)
            return [p["data"]["username"], p["data"]["user_id"]]
        except:
            return -1
    def get_unlikes(self):
        try:
            url="http://code.xueersi.com/api/compilers/"+str(self.pid)+"?id="+str(self.pid)
            headers = {'Content-Type':'application/json'}
            a=requests.get(url=url, headers=headers)
            null,false,list_get,string=0,0,[],''
            p=json.loads(a.text)
            unlikes=p["data"]["unlikes"]
            return unlikes
        except:
            return -1
    def get_description(self):
        try:
            url='https://code.xueersi.com/api/compilers/v2/'+str(self.pid)+'?id='+str(self.pid)
            a=json.loads(urllib.request.urlopen(url).read().decode())
            return a['data']['description']
        except:
            return -1
    def get_codexml(self):
        try:
            url='https://code.xueersi.com/api/compilers/v2/'+str(self.pid)+'?id='+str(self.pid)
            a=json.loads(urllib.request.urlopen(url).read().decode())
            return a['data']['xml']
        except:
            return -1
    def get_name_as_pid(self):
        try:
            url='https://code.xueersi.com/api/compilers/v2/'+str(self.pid)+'?id='+str(self.pid)
            a=json.loads(urllib.request.urlopen(url).read().decode())
            return a['data']['name']
        except:
            return -1

    def is_like(self):
        url='http://code.xueersi.com/api/compilers/v2/'+str(self.pid)+'?id='+str(self.pid)
        data=json.loads(urllib.request.urlopen(url).read().decode())
        like1 = data['data']['likes']
        unlike1 = data['data']['unlikes']
        import time
        time.sleep(1)
        url='http://code.xueersi.com/api/compilers/v2/'+str(self.pid)+'?id='+str(self.pid)
        while 1:
            data=json.loads(urllib.request.urlopen(url).read().decode())
            like2 = data['data']['likes']
            unlike2 = data['data']['unlikes']
            if like2>like1:
                return 0
            elif unlike1>unlike2:
                return -1
            elif like1==like2 and unlike1==unlike2:
                return 1
def help():
    print(urllib.request.urlopen('http://www.asunc.cn/alsoxeshelp.txt').read().decode("gbk"))


import sys
def getCookies():
    cookies = ""
    if len(sys.argv) > 1:
        try:
            cookies = json.loads(sys.argv[1])["cookies"]
        except:
            pass
    return cookies

def jsonLoads(str):
    try:
        return json.loads(str)
    except:
        return None
import requests
import json

# from calendar import c

import requests
import json


def get_api(http,*w):
	s = requests.Session()
	header = {'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate',
			  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
			  'Cookie': 'xesId=b524835904a4a420cba3dde34890bade; user-select=scratch;  xes_run_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIuY29kZS54dWVlcnNpLmNvbSIsImF1ZCI6Ii5jb2RlLnh1ZWVyc2kuY29tIiwiaWF0IjoxNjAxODA5NDcxLCJuYmYiOjE2MDE4MDk0NzEsImV4cCI6MTYwMTgyMzg3MSwidXNlcl9pZCI6bnVsbCwidWEiOiJNb3ppbGxhXC81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXRcLzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZVwvODUuMC40MTgzLjEyMSBTYWZhcmlcLzUzNy4zNiBFZGdcLzg1LjAuNTY0LjY4IiwiaXAiOiIxMTIuNDkuNzIuMTc1In0.9bXcb813GhSPhoUJkezZpV8O50ynm0hhYvszNyczznQ; prelogid=ef8f6d12febabf75bf9599744b73c6f5; xes-code-id=87f66376f1afd34f70339baeca61b7a1.8dbd833da9122d69a17f91054066dbb3; X-Request-Id=82f1c3968c8ff01ee151a0413f56aa84; Hm_lpvt_a8a78faf5b3e92f32fe42a94751a74f1=1601809487',
			  'Host': 'code.xueersi.com', 'Proxy-Connection': 'keep-alive',
			  'Referer': 'http://code.xueersi.com/space/11909587',
			  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68'}
	total = json.loads(_nice(s.get(http, headers=header).text))
	return total
def _nice(emoji_str):
	import struct
	return ''.join(
		c if c <= '\uffff' else ''.join(chr(x) for x in struct.unpack('>2H', c.encode('utf-16be'))) for c in emoji_str)
def get_fans_info(id, lengh=None):
	id = str(id)
	# page = 1
	if lengh == None:
		lengh = (int(get_info(id)["fans"])//150)+1
	c=[]
	for x in range(lengh):
		# headers = {'Content-Type': 'application/json'}
		total = get_api(f"http://code.xueersi.com/api/space/fans?user_id={id}&page={str(x+1)}&per_page=150")
		c+=total["data"]["data"]

	return c
def get_follows_info(id, lengh=None):
	id = str(id)
	page = 1
	if lengh == None:
		lengh = get_info(id)["follows"]

	total = get_api(
		"http://code.xueersi.com/api/space/follows?user_id=" + id + "&page=" + str(page) + "&per_page=" + str(lengh))
	return total["data"]["data"]
def get_info(id):
	s = requests.Session()
	headers = {'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Cookie': 'xesId=b524835904a4a420cba3dde34890bade; user-select=scratch;  xes_run_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIuY29kZS54dWVlcnNpLmNvbSIsImF1ZCI6Ii5jb2RlLnh1ZWVyc2kuY29tIiwiaWF0IjoxNjAxODA5NDcxLCJuYmYiOjE2MDE4MDk0NzEsImV4cCI6MTYwMTgyMzg3MSwidXNlcl9pZCI6bnVsbCwidWEiOiJNb3ppbGxhXC81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXRcLzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZVwvODUuMC40MTgzLjEyMSBTYWZhcmlcLzUzNy4zNiBFZGdcLzg1LjAuNTY0LjY4IiwiaXAiOiIxMTIuNDkuNzIuMTc1In0.9bXcb813GhSPhoUJkezZpV8O50ynm0hhYvszNyczznQ; prelogid=ef8f6d12febabf75bf9599744b73c6f5; xes-code-id=87f66376f1afd34f70339baeca61b7a1.8dbd833da9122d69a17f91054066dbb3; X-Request-Id=82f1c3968c8ff01ee151a0413f56aa84; Hm_lpvt_a8a78faf5b3e92f32fe42a94751a74f1=1601809487', 'Host': 'code.xueersi.com', 'Proxy-Connection': 'keep-alive', 'Referer': 'http://code.xueersi.com/space/11909587', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68'}

	total = json.loads(
		_nice(s.get("http://code.xueersi.com/api/space/profile?user_id=" + str(id), headers=headers).text))[
		"data"]
	return {
		# "user_id": total["user_id"],
		"name": total["realname"],
		"slogan": total["signature"],
		"fans": total["fans"],
		"follows": total["follows"],
		"icon": total["avatar_path"]
	}
def get_user_id(id):
	id = id.split("&pid=")[1].split("&")[0]
	url = "http://code.xueersi.com/api/compilers/" + id + "?id=" + id
	a = get_api(url)
	# self._nice()
	return a["data"]["user_id"]
class user:
	def __init__(self, id):
		s = requests.Session()
		id = str(id)
		url = "http://code.xueersi.com/api/space/index?user_id=" + id
		headers ={'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Cookie': 'xesId=b524835904a4a420cba3dde34890bade; user-select=scratch; userGrade=8; wx=408f3d126b6e5da40f1231f4a8e82cecmqx0f94f4q; Hm_lvt_a8a78faf5b3e92f32fe42a94751a74f1=1600492811,1600492816; xes-code-id=87f66376f1afd34f70339baeca61b7a1.8dbd833da9122d69a17f91054066dbb3; prelogid=82f1c3968c8ff01ee151a0413f56aa84; xes_run_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIuY29kZS54dWVlcnNpLmNvbSIsImF1ZCI6Ii5jb2RlLnh1ZWVyc2kuY29tIiwiaWF0IjoxNjAxODA5NDg4LCJuYmYiOjE2MDE4MDk0ODgsImV4cCI6MTYwMTgyMzg4OCwidXNlcl9pZCI6bnVsbCwidWEiOiJNb3ppbGxhXC81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXRcLzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZVwvODUuMC40MTgzLjEyMSBTYWZhcmlcLzUzNy4zNiBFZGdcLzg1LjAuNTY0LjY4IiwiaXAiOiIxMTIuNDkuNzIuMTc1In0.Depgg9J-Hbe5RDeQvQwn59Aj0aa4CnndKeOKad-5WTY; X-Request-Id=db987fe27cbc7c51525a99c6419a34c7; Hm_lpvt_a8a78faf5b3e92f32fe42a94751a74f1=1601810095', 'Host': 'code.xueersi.com', 'Proxy-Connection': 'keep-alive', 'Referer': 'http://code.xueersi.com/space/11909587', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68'}
		a = s.get(url=url, headers=headers)
		a = json.loads(_nice(a.text))
		a = a["data"]
		self.data = a
		self.works = a["works"]["total"]
		self.fans = a["fans"]["total"]
		self.follows = a["follows"]["total"]
		self.overview = a["overview"]
		self.like_num = self.overview["likes"]
		self.view_num = self.overview["views"]
		self.work_num = self.overview["works"]
		self.favorites = self.overview["favorites"]
#nice
#
# # a = user(get_user_id(
# # 	"http://code.xueersi.com/home/project/detail?lang=code&pid=6076813&version=offline&form=python&langType=python"))
# # print(a.work_info)
def get_fansnum(id):
    try:
        url = "http://code.xueersi.com/api/space/fans?user_id=" + str(id) + "&page=1&per_page=10"
        num = json.loads(requests.get(url).text)["data"]["total"]
        return num
    except:
        return -1
def getnowuser():
    try:
        a = getCookies()
        num = a.index("stu_id=") + 7
        id = ""
        for i in range(num, num + 100):
            if a[i] != ";":
                id = id + a[i]
            else:
                break
        try:
            user_info = get_info(id)
        except:
            user_info={"name":id+"号未知用户"}
            # 获取这个人的大部分信息，返回一个字典
            #:返回这个人的名字
        return {'state':True,'user_id':id, "user_name":user_info["name"]}
    except:
        return {"state":False,'user_id':"未登录","user_name":"未登录"}
