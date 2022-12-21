import requests
base_url='http://localhost:5000/api/'
test = {
    'title': 'this is the title',
    'lyrics': 'omg this a song is so wow again'
}
x = requests.post(f'{base_url}song/new', json = test, )

print(x.text)