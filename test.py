from requests import get, post, delete

print(get('http://localhost:5000/api/v2/users/1').json())

print(get('http://localhost:5000/api/v2/users/-1').json())
# non-existent id

print(get('http://localhost:5000/api/v2/users/qwe').json())
# not int

print(delete('http://localhost:5000/api/v2/users/1').json())

print(delete('http://localhost:5000/api/v2/users/-1').json())
# non-existent id

print(delete('http://localhost:5000/api/v2/users/qwe').json())
# not int


print(get('http://localhost:5000/api/v2/users').json())


print(post('http://localhost:5000/api/v2/users',
           json={
               'name': 'John',
               'about': 'singer, actor',
               'email': 'john@mail.com'
           }).json())

print(post('http://localhost:5000/api/v2/users', json={}).json())
# empty request

