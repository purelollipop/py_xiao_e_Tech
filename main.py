import requests
import pprint
import base64
import re
from Crypto.Cipher import AES
import multiprocessing

title = "7AIgorithm Tricks II"
url = "https://btt-vod.xiaoeknow.com/529d8d60vodtransbj1252524126/37132cac387702304714704851/drm/v.f421220_0.ts"
reqObj = {
    "start": 0,
    "end": 0,
    "type": "mpegts",
    "sign": "0c977b894a24956956d945b46d5de933",
    "t": "63e661a0",
    "us": "MpskGdNyYM",
}

headers = {
    "authority": "btt-vod.xiaoeknow.com",
    "method": "GET",
    "path": f"/529d8d60vodtransbj1252524126/375c91ec387702304714746332/drm/v.f421220_0.ts?start={reqObj['start']}&end={reqObj['end']}&type={reqObj['type']}&sign={reqObj['sign']}&t={reqObj['t']}&us={reqObj['us']}",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "origin": "https: //xiaoe.kaikeba.com",
    "pragma": "no-cache",
    "referer": "https://xiaoe.kaikeba.com/",
    "sec-ch-ua": '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78"
}

urlList = []

url2 = "https://app.xiaoe-tech.com/xe.basic-platform.material-center.distribute.vod.pri.get/1.0.0"
reque2Obj = {
    "app_id": "",
    "mid": "",
    "urld": "",
    "uid": "u_63311fa665d9b_7cIbMVhmV4",
}
headers2 = {
    "authority": "app.xiaoe-tech.com",
    "method": "GET",
    "path": f"/xe.basic-platform.material-center.distribute.vod.pri.get/1.0.0?app_id={reque2Obj['app_id']}&mid={reque2Obj['mid']}&urld={reque2Obj['urld']}&uid={reque2Obj['uid']}",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "origin": "https://xiaoe.kaikeba.com",
    "pragma": "no-cache",
    "referer": "https://xiaoe.kaikeba.com/",
    "sec-ch-ua": '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78"
}

base64_key = ""


# 获取密钥
def originFun():
    response = requests.get(url=url2, params=reque2Obj, headers=headers2)
    print(f"Content-Length----{response.headers['Content-Length']}")
    if len(response.content) > 16:
        print(f"长度错误{len(response.content)},应该是16才对")
    else:
        result_list = []
        userid_bytes = bytes(reque2Obj["uid"].encode(encoding='utf-8'))
        print(f"userid_bytes---{userid_bytes}")
        for index in range(0, len(response.content)):
            # print(index)
            result_list.append(
                response.content[index] ^ userid_bytes[index])
        print(result_list)
        global base64_key
        # base64_key = base64.b64encode(bytes(result_list)).decode()
        base64_key = bytes(result_list)
        # print(f"base64_key----{base64_key}")


# 获取m3文件片段 ，获取requesObj2的关键参数  http://mirrors.aliyun.com/pypi/simple/
#  --trusted-host mirrors.aliyun.com  https://pypi.python.org/simple
def splitUrlFun():
    with open("./src/dist/url/text1", "r") as f:
        ff = f.read()
        ff2 = (ff.split("v.f421220_0.ts?"))
        i = 0
        # print(ff2[0])
        app_id = re.findall("app_id=((\w){1,})&", ff2[0])
        mid = re.findall("mid=((\w){1,})&", ff2[0])
        urld = re.findall("urld=((\w){1,})\"", ff2[0])
        reque2Obj["app_id"] = app_id[0][0]
        reque2Obj["mid"] = mid[0][0]
        reque2Obj["urld"] = urld[0][0]
        print(f"app_id```{app_id}````{reque2Obj['app_id']}")
        print(f"mid```{mid}````{reque2Obj['mid']}")
        print(f"urld```{urld}````{reque2Obj['urld']}")
        for strdata in ff2:
            if i > 0:
                str2 = strdata.split("&")
                obj = {
                    "start": str2[0].split("start=")[1],
                    "end": str2[1].split("end=")[1],
                    "dat": None
                }
                urlList.append(obj)
            i += 1


def allGetMvFun():
    if base64_key:
        aes = AES.new(key=base64_key, IV=b"0000000000000000", mode=AES.MODE_CBC)
        for i in urlList:
            reqObj["start"] = int(i["start"])
            reqObj["end"] = int(i["end"])
            # mu = multiprocessing.Process(target=getMvFun, args=(reqObj, headers, aes,i))
            # mu.start()
            response = requests.get(url=url, params=reqObj, headers=heads)

        print("下载完成，ok")


# 开始获取mv
def getMvFun(reqObj, heads, aes, obj):
    response = requests.get(url=url, params=reqObj, headers=heads)
    if response.status_code == 200:
        obj["dat"] = aes.decrypt(response.content)
        # fileWriteFun(aes.decrypt(response.content))
    else:
        print(f"获取异常。{response},下载失败")


# 写入文件操作
def fileWriteFun():
    # f = open(f"./src/dist/mv/{title}.mp4", mode="ab")
    print(len(urlList))
    i = 0

    while True:
        if i < len(urlList):
            if urlList[i]["dat"]:
                print(urlList[i])
                print(i)
                print(i >= len(urlList))
                i += 1
        else:
            print("到结尾了")
            break
        # if urlList[i].data:
        # f.write(response)
        # f.flush()
    print("写完了")
    # f.close()


splitUrlFun()
originFun()
allGetMvFun()
fileWriteFun()
