import requests
import json
from tempmail import genmail, getmail
import time
from tenacity import retry

pattern = "openex"
email_url = "https://oex-hub-app-api-dot-elite-crossbar-345112.uc.r.appspot.com/mail/get/email"

request_url = "https://oex-hub-app-api-dot-elite-crossbar-345112.uc.r.appspot.com/mail/request/code"

bind_url = "https://oex-hub-app-api-dot-elite-crossbar-345112.uc.r.appspot.com/mail/bind/email"

confirm_url = "https://oex-hub-app-api-dot-elite-crossbar-345112.uc.r.appspot.com/oex/confirmTotalAirdrop"

headers = {
    'Host': 'oex-hub-app-api-dot-elite-crossbar-345112.uc.r.appspot.com',
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/4.9.2'
}
null_data = '{"doc":null}'
def email_check(data):
  data = json.dumps(data)
  r = requests.post(email_url, headers=headers, data=data)
  #print(r.text)
  if null_data in r.text:
    return 1
  else:
    return 0
    
def send(data, email):
  email_dict = {'email': f'{email}'}
  data.update(email_dict)
  data = json.dumps(data)
  requests.post(request_url, headers=headers, data=data)
  
def code(data, email, code):
    email_code_dict =  {'email': f'{email}', 
    'code': f'{code}'}
    data.update(email_code_dict)
    data = json.dumps(data)
    r = requests.post(bind_url, headers=headers, data=data)
    if r.status_code == 200:
      print("success")

def checkpoint(check=None, iter=None):
    if check =="save" and iter:
        with open("checkpoint", "w") as f:
            f.write(iter)
    if check == "ask":
        try:
            with open("checkpoint", "r") as f:
                buffer = f.read()
                return buffer
        except Exception:
            return 0

  
  
@retry
def per_iter(data):
  mail = genmail()
  if email_check(data):
    send(data, mail)
    print("mail sent")
    time.sleep(10)
    res = getmail(mail, pattern)
    if res:
      mail_code = res['textBody']
      mail_code = mail_code.split()
      mail_code = mail_code[4]
      code(data, mail, mail_code)
    else:
      raise
  else:
    print("skipped")
      
def run():
  iter = checkpoint(check="ask")
  with open("new_gen_data.txt", "r") as f:
    tok_list = f.readlines()
    tok_list = [x.strip() for x in tok_list]

    for acc in range(int(iter), len(tok_list)):
      data = json.loads(tok_list[acc])
      per_iter(data)
      print("iter : " + str(acc))
      checkpoint(check="save", iter=str(acc))
      
      
run()
      
      
