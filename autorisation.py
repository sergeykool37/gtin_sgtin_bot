import requests
import fake_useragent
import json
url = 'https://back-gateway.pharm-portal.ru/sso/login'
login = "sergeykool37@gmail.com"
password = "968577aaa"



def autorisation(url, login, password):
    data = dict(
        email = login,
        password = password)

    user = fake_useragent.UserAgent().random
    headers = {
        'user-agent': user
    }

    session = requests.Session()
    session.headers['Content-Type'] = 'application/json; charset=utf-8'
    responcse = session.post(url, data=json.dumps(data), headers=headers)



    return session

if __name__ =='__main__':
    autorisation(url, login, password)