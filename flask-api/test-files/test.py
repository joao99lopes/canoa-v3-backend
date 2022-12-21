import requests
base_url='http://localhost:5000/api/'
test = {
    'title': 'this is the title',
    'lyrics': 'omg this a song is so wow again'
}

# test = {
#     'first_name': 'Maria',
#     'last_name': 'Balsinhas',
#     'email': 'drabrinquedos@gmail.com',
#     'password': 'password'
# }

x = requests.post(f'{base_url}song/new', json = test, )

print(x.text)