from pprint import pprint
from requests import get, post, delete

pprint(get('http://127.0.0.1:8080/api/v2/users').json())
pprint(get('http://127.0.0.1:8080/api/v2/users/2').json())
pprint(get('http://127.0.0.1:8080/api/v2/users/100').json())
# pprint(get('http://127.0.0.1:8080/api/v2/users/qqq').json())

pprint(post('http://127.0.0.1:8080/api/v2/users', json={}).json())
pprint(post('http://127.0.0.1:8080/api/v2/users', json={'name': 'Paul'}).json())
pprint(post('http://127.0.0.1:8080/api/v2/users', json={'name': 'Paul', 'position': 'warrior',
                                                        'surname': 'Atreides', 'age': 17, 'address': 'dune',
                                                        'speciality': 'mystic',
                                                        'hashed_password': 'paul', 'email': 'paul@mars.org'}).json())
pprint(get('http://127.0.0.1:8080/api/v2/users/4').json())

pprint(delete('http://127.0.0.1:8080/api/v2/users/999').json())
# pprint(delete('http://127.0.0.1:8080/api/v2/users/4').json())