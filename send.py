# -*- coding: utf8 -*-
# python >=3.8
import requests,json,time,random
corpid = os.environ.get("corpid")
corpsecret = os.environ.get("corpsecret")
tgbotoken = os.environ.get("tgbotoken")
chatid =os.environ.get("chatid")
key = os.environ.get("key")
sckey = os.environ.get("sckey")

now = time.strftime("🎃 %Y-%m-%d %H:%M:%S 🎃\n\n", time.localtime())
msg =""

def lt() :
  r = requests.get("https://cdn.jsdelivr.net/gh/Ysnsn/source/list.txt").text
  return random.choice(r.split('\n'))

a = lt()

def push_wx(msg):
  if corpid == '' or corpsecret == '':
    print("[注意] 未提供corpid or corpsecret ，推送个🍗！请别开玩笑了")
  else:
    server_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
    re = requests.post(server_url)
    jsontxt = json.loads(re.text)
    access_token = jsontxt['access_token']
    html = msg.replace('\n', '<br>')
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    data ={"touser" : "@all",
           "msgtype" : "mpnews",
           "agentid" : "1000002",
           "mpnews" : {
                 "articles" : [
                       {
                            "title" : "🥱文案推送官🥱",
                             "content" : html,
                             "author" : "智能推送助手",
                             "thumb_media_id": a,
                             "content_source_url" : "",
                             "digest" : msg
                        }
                               ]
                       },
           "safe": 0
          }

    send_msges=(bytes(json.dumps(data), 'utf-8'))
    res = requests.post(url, send_msges)
    respon = res.json()   #当返回的数据是json串的时候直接用.json即可将respone转换成字典

    if respon['errmsg'] == "ok":
        print(f"企业微信推送成功\n")
    else:
         print(f" 推送失败:鬼知道哪错了\n")
         print(respon)
        

## 推送QQ
def push_qq(msg):
    """
    推送消息到QQ酷推
    """
    if key == '':
        print("[注意] 未提供Qmsgkey，推送！个🍗")
    else:
        server_url = f"https://qmsg.zendee.cn/group/{key}?"
        params = {
             "msg": msg
        }
      
        response = requests.get(server_url, params=params)
        json_data = response.json()
        if json_data['reason'] == "操作成功":
            print(f"推送成功")
        else:
            print(f" 推送失败:鬼知道哪错了")
            print(json_data)    
# 推送server
def push_wxs(msg):
    """
    推送消息到微信
    """
    if sckey == '':
        print("[注意] 未提供sckey，推送个🍗！")
    else:
        html = msg.replace('\n', '<br>')
        server_url = f"https://sc.ftqq.com/{sckey}.send"
        params = {
            "text": '测试消息',
            "desp": html
        }
 
        response = requests.get(server_url, params=params)
        json_data = response.json()
 
        if json_data['errno'] == 0:
            print(f"推送成功。")
        else:
            print(f"推送失败：{json_data['errno']}({json_data['errmsg']})")

def push_tg(msg):
    if tgbotoken == '' or chatid == '':
       print("[注意] 未提供TG key，推送！个🍗别开玩笑了")
    else:
       url=f"https://tgpush.wyang.workers.dev/bot{tgbotoken}/sendMessage?parse_mode=Markdown&text={msg}&chat_id={chatid}"
       res = requests.get(url)
       re= res.json()
      # print(re)
       if re['ok'] == True :
             print("Tg：发送成功")
       else :
             print("Tg：发送失败!")
             print(re)

def send(msg):
   msg = now+ msg
   push_tg(msg)
   push_qq(msg)
   push_wx(msg)

