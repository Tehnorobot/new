from requests import post, get, delete

# Пустой запрос
print(post('http://localhost:8080/api/v2/jobs').json())
# Неполный запрос
print(post('http://localhost:8080/api/v2/jobs',
           json={'title': 'Заголовок'}).json())
# Запрос с существующим id
print(post('http://localhost:8080/api/v2/jobs',
           json={'id': 3,
                 'team_leader': 1,
                 'job': 'Сделать дз',
                 'work_size': 35,
                 'collaborators': "",
                 'if_finished': True}).json())

id = 638
# Правильный запрос
print(post('http://localhost:8080/api/v2/jobs',
           json={'id': id,
                 'team_leader': 3,
                 'job': 'Сделать дз',
                 'work_size': 35,
                 'collaborators': "",
                 'if_finished': True}).json())

print(get(f'http://localhost:8080/api/v2/jobs/{id}').json())

print(delete(f'http://localhost:8080/api/v2/jobs/{id}').json())