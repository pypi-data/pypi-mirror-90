from urllib import parse
import urllib,pygame,os
import contextlib
import wave
import urllib.request
import requests,json
import time
from os import path
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.parse import quote_plus
import hashlib
import random
import base64
import json,time,socket
speaker=1
ak=urllib.request.urlopen("http://www.asunc.cn/ak.txt").read().decode("utf-8")
ak=json.loads(ak)['ak']
class Alsoai():
    def __init__(self):
                self.availble = True
    def get_ipaddress(self,ip, getpoint=False):
        if self.availble!=True:
            return -2
        else:
            if ip.count(".") != 3:
                return -1
            else:
                url = 'http://api.map.baidu.com/location/ip?ak=' + ak + '&ip=' + urllib.parse.quote(ip) + '&coor=bd09ll'
                address = urllib.request.urlopen(url).read().decode("utf-8")
                if True:
                    address = json.loads(address)
                    if address['status'] == 0:
                        if getpoint==True:
                            content = address['content']
                            addrpoint = content['point']
                            return content['address'], addrpoint['x'], addrpoint['y']
                        else:
                            content = address['content']
                            return content['address']

                    else:
                        return -1
    def get_traffic(self,road,city):
        if self.availble != True:
            return -2
        else:
            url='http://api.map.baidu.com/traffic/v1/road?road_name='+urllib.parse.quote(road)+'&city='+urllib.parse.quote(city)+'&ak='+ak
            address = urllib.request.urlopen(url).read().decode("utf-8")
            address = json.loads(address)
            if address['status']==0:
                return address['description']
            else:
                return -1
    def makevoice(self,text, filename,mode=1,speed=40):
        if self.availble != True:
            return -2
        else:
            def getReqSign(params, key):
                dict_kl = sorted(params)
                s = ''
                for k in dict_kl:
                    v = params[k]
                    if v != '':
                        v0 = str(quote_plus(str(v)))
                        s = s + k + '=' + v0 + '&'
                s = s + 'app_key=' + key;
                m = hashlib.md5()
                m.update(s.encode("utf8"))
                sign = m.hexdigest()
                sign = sign.upper()
                return sign
            app={'appid':'2155851121','appkey':'GRsIdG8kvCydBN4z'}
            appid = app['appid']
            appkey = app['appkey']
            url = 'https://api.ai.qq.com/fcgi-bin/aai/aai_tts'
            time_s = int(time.time())
            m = hashlib.md5()
            m.update(str(time_s).encode("utf8"))
            nonce_s = m.hexdigest()
            nonce_s = nonce_s[0:random.randint(1, 31)]
            vmv='1'
            filename=str(filename)
            text=str(text)
            if filename[len(filename)-4]=='.':
                if filename[len(filename)-3]=='p' or filename[len(filename)-3]=='P':
                    wmv='1'
                elif filename[len(filename)-3]=='w' or filename[len(filename)-3]=='W':
                    wmv='2'
                elif filename[len(filename)-3]=='m' or filename[len(filename)-3]=='M':
                    wmv='3'

            params = {'app_id': appid,
                      'speaker': mode,
                      'format': wmv,
                      'volume': '0',
                      'speed': speed * 2,
                      'text': text,
                      'aht': '0',
                      'apc': '58',
                      'time_stamp': time_s,
                      'nonce_str': nonce_s,
                      'sign': ''
                      }
            params['sign'] = getReqSign(params, appkey)
            s = urlencode(params)
            res = urlopen(url, s.encode())  # 网络请求
            res_str = res.read().decode()
            res_dict = eval(res_str)

            if res_dict['ret'] == 0:
                res_data = res_dict['data']
                res_data_format = res_data['format']
                res_data_speech = res_data['speech']
                res_data_md5sum = res_data['md5sum']
                filepath = path.dirname(__file__)  # 目录
                file = '/wav01.wav'
                base64_data = res_data_speech
                ori_image_data = base64.b64decode(base64_data)
                fout = open(filename, 'wb')
                fout.write(ori_image_data)
                fout.close()
                return res_dict['ret']
            else:
                return -1
    def speak(self,text,mode=1,speed=40):
        if self.availble != True:
            return -2
        else:
            def getReqSign(params, key):
                dict_kl = sorted(params)
                s = ''
                for k in dict_kl:
                    v = params[k]
                    if v != '':
                        v0 = str(quote_plus(str(v)))
                        s = s + k + '=' + v0 + '&'
                s = s + 'app_key=' + key;
                m = hashlib.md5()
                m.update(s.encode("utf8"))
                sign = m.hexdigest()
                sign = sign.upper()
                return sign
            app={'appid':'2155851121','appkey':'GRsIdG8kvCydBN4z'}
            appid = app['appid']
            appkey = app['appkey']
            url = 'https://api.ai.qq.com/fcgi-bin/aai/aai_tts'
            time_s = int(time.time())
            m = hashlib.md5()
            m.update(str(time_s).encode("utf8"))
            nonce_s = m.hexdigest()
            nonce_s = nonce_s[0:random.randint(1, 31)]
            params = {'app_id': appid,
                      'speaker': mode,
                      'format': '2',
                      'volume': '0',
                      'speed': speed*2,
                      'text': text,
                      'aht': '0',
                      'apc': '58',
                      'time_stamp': time_s,
                      'nonce_str': nonce_s,
                      'sign': ''
                      }
            params['sign'] = getReqSign(params, appkey)
            s = urlencode(params)
            res = urlopen(url, s.encode()).read().decode()
            res_dict = eval(res)
            if res_dict['ret'] == 0:
                res_data = res_dict['data']
                res_data_format = res_data['format']
                res_data_speech = res_data['speech']
                res_data_md5sum = res_data['md5sum']
                filepath = path.dirname(__file__)  # 目录
                file = '/wav01.wav'
                base64_data = res_data_speech
                ori_image_data = base64.b64decode(base64_data)
                try:
                    with open('alsovoice.wav', "wb") as f:
                        f.write(ori_image_data)
                    f.close()
                    import wave
                    fr = wave.open('alsovoice.wav', 'rb')
                    secs = fr.getnframes() / fr.getframerate()
                    fr.close()
                    pygame.mixer.init()
                    pygame.mixer.music.load("alsovoice.wav")
                    pygame.mixer.music.play()
                    time.sleep(secs+0.1)
                    return res_dict['ret']
                except:
                    return -1
            else:
                return -1
    def AI_chat(self,text,mode=5):
        if self.availble != True:
            return -2
        else:
            def getReqSign(params, key):
                dict_kl = sorted(params)
                s = ''
                for k in dict_kl:
                    v = params[k]
                    if v != '':
                        v0 = str(quote_plus(str(v)))
                        s = s + k + '=' + v0 + '&'
                s = s + 'app_key=' + key;
                m = hashlib.md5()
                m.update(s.encode("utf8"))
                sign = m.hexdigest()
                sign = sign.upper()
                return sign

            app={'appid':'2155851121','appkey':'GRsIdG8kvCydBN4z'}
            appid = app['appid']
            appkey = app['appkey']
            url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
            time_s = int(time.time())
            m = hashlib.md5()
            m.update(str(time_s).encode("utf8"))
            nonce_s = m.hexdigest()
            nonce_s = nonce_s[0:random.randint(1, 31)]
            params = {'app_id': appid,
                      'time_stamp': time_s,
                      'nonce_str': nonce_s,
                      'session': '0',
                      'sign': '',
                      'question': text
                      }
            params['sign'] = getReqSign(params, appkey)
            s = urlencode(params)
            res = urlopen(url, s.encode())  # 网络请求
            res_str = res.read().decode()
            res_dict = eval(res_str)
            if res_dict['ret']==0:
                return 0,res_dict['data']['answer']
            else:
                if res_dict['ret'] == 16394:
                    return 404
    def get_pcsystem(self):
        import platform
        return platform.system()

