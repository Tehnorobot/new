from requests import get


print(get('http://localhost:8080/api/v2/jobs').json())
print(get('http://localhost:8080/api/v2/jobs/3').json())
print(get('http://localhost:8080/api/v2/jobs/0').json())
print(get('http://localhost:8080/api/v2/jobs/sdf'))