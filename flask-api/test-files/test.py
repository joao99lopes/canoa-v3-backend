import requests
base_url='http://localhost:5000/api/'

# for i in range(20):
lyrics = "aaa"

for i in range(10):
    lyrics += f"\n{i}"
for i in range(3):
    lyrics += f"\n{lyrics}"
test = {
    'title': f'teste lyrics grande7',
    'lyrics': lyrics
}

# test = {
#     'first_name': 'Maria',
#     'last_name': 'Balsinhas',
#     'email': 'drabrinquedos@gmail.com',
#     'password': 'password'
# }

x = requests.post(f'{base_url}song/new', json = test, )

print(x.text)