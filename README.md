![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-%23FCC624.svg?style=for-the-badge&logo=sqlalchemy&logoColor=black)
[![Swagger](https://img.shields.io/badge/swagger-%23857E3.svg?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)


# Домашка по SQLAlchemy 

Как завести все?

Клонируем репозиторий:
```bash
git clone git@github.com:Amir800S/sqlalchemy_homework.git
```
Переходим в директорию:
```python
cd sqlalchemy_homework
```
Переходим в папку infra:
```python
cd infra 
```
Запускаем файл Docker:
```python
sudo docker compose up 
```
### Также есть скрипт load_data.py который добавит данные в базу данных:
```python
python3 load_data.py
```

### К проекту подключена автоматическая документация Swagger:
```python
http://localhost:8000/apidocs/
```

### Все работает и доступно по адресу:
```python
http://localhost:8000
```