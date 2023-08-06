import requests,json
class alsoQQ:
    def __init__(self,qq):
        self.qq=str(qq)
    def get_qqname(self):
        url="https://api.uomg.com/api/qq.info?qq="+self.qq
        qqim=requests.get(url)
        qqim.encoding="gbk"
        string=json.loads(qqim.text)
        return string['name']
    def get_qqimageurl(self):
        url="https://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?g_tk=1518561325&uins="+self.qq
        qqim=requests.get(url)
        qqim.encoding="gbk"
        string=qqim.text
        string=string.replace("portraitCallBack(","")
        string=string.replace(")","")
        return json.loads(string)[self.qq][0]
    def get_qqlvzuan(self):
        url="https://api.uomg.com/api/qq.info?qq="+self.qq
        qqim=requests.get(url)
        qqim.encoding="gbk"
        string=qqim.text
        return json.loads(string)['lvzuan']