# Serials Box
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

### Description
Serials box is an online service for information related to television series - including cast,
crew and personal biographies, plot summaries, and where users can leave comments and write articles about the series.

### Website address
http://84.252.143.63/

### Features
Series pages and the blog are available to all users, but only registered and logged in users can leave comments on the series and add new articles to the blog. Registered users can add series to their favorites and like articles.

Each registered user has access to a personal account, where he can change his username, add an avatar, write information about himself and set his date of birth.
On the profile page, the user has access to articles they like, favorite series, and adding an article. The article can be deleted and edited only by the author of the article and the admin.

User profile page show a user's registration date and username and, optionally, their avatar, bio and age.

## Technologies:
- Python 3.9
- Django 3.2.8
- Nginx
- Gunicorn
- PostgreSQL
- Docker, docker-compose
- Yandex.Cloud

## Prerequisites:
Docker and Docker-Compose must be installed.
### Installation instructions
- [Docker](https://docs.docker.com/get-docker/)
- [Docker-Compose](https://docs.docker.com/compose/install/)

## Setup:
- Clone the github repository:
```bash
$ git clone https://github.com/IlyaKhramtsov/serials-box.git
```
- Enter the project directory:
```bash
$ cd serials-box/
```
- Create an ```.env``` file in the current directory, add the environment variables there 
as in the ```.env.template``` file from this repository.

- Start docker-compose:
```bash
$ docker-compose -f docker-compose.yml up -d
```
- Create superuser:
```bash
$ docker-compose -f docker-compose.yml run --rm web python manage.py createsuperuser
```