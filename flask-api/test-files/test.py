import requests

test = {
    'title': 'this is afaa new svasfsaassdsdtitle',
    'lyrics': 'omg this afsfasfsong is sosdafgsdg wow again'
}
x = requests.get('http://localhost:5000/api/song/get_title_from_text', json = test, )

print(x.text)