# Docker-Hosting
Проект хостинга для docker контейнеров. 

## Содержание
- [Технологии](#технологии)
- [Локальный запуск](#локальный-запуск)
- [Актуальность](#актуальность)
- [Команда проекта](#команда-проекта)

## Технологии
- [Django](https://www.djangoproject.com/)
- [Python](https://www.python.org/)
- [Bootstrap5](https://www.creative-tim.com/)
- [CreativeTeam](https://www.creative-tim.com/)
- [Python Docker SDK](https://docker-py.readthedocs.io/)
- [Celery Task Queue](https://docs.celeryq.dev/en/stable/)
- [Django Channels](https://channels.readthedocs.io/en/latest/)
- [PostgreSQL](https://www.postgresql.org/)
- [Reddis](https://redis.io/docs/latest/)

## Результат 
Видео работы сайта доступно по ссылке: https://youtu.be/TDW2EhnFuPQ

В связи с блокировкой Docker Hub для российских пользователей развертывание проекта откладывается на неопределенный срок
## Локальный запуск
### Локальный запуск: dev containers (рекомендуемый нужен только Docker Desktop)
```sh
Установите Docker Desktop 
Воспользуйтесь руководством по установки прокси huecker (https://huecker.io/) или используйте ВПН
Откройте проект в VS code и оставьте Docker Desktop открытым
```
1 Запуск дев контейнера в vs code
```sh
cntrl + shift + p
open folder in container
```
2 Ждем 
```sh
параметры запуска уже настроены
после запуска начинаем работать
```
3 В боковой пани находим Run and debug 
```sh
запускаем Run Server для запуска сервера
запускаем Migrate для миграции 
запускаем Run Celery worker  и Run Celery Beat для асинхронных задач 
```
4 Выход
```sh
cntrl shift p
reopen localy
```
### Локальный запуск бе dev containers (возможный но не рекомендуемый способ)
```sh
Установите Docker Desktop 
Воспользуйтесь руководством по установки прокси huecker (https://huecker.io/) или используйте ВПН
```
1 Создение виртуальной среды для python venv
```sh
py -m venv .venv
```
2 Активировать venv
```sh
 .venv\Scripts\Activate.ps1
```
3 Установка зависимостей 
```sh
pip install -r requirements.txt
```
4 Установить Postgres и Reddis и поменять settings.py 
```sh
# Celery settings
CELERY_BROKER_URL = "redis://redis:6379" 
CELERY_RESULT_BACKEND = "redis://redis:6379"
#заменить на 
# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
```
5 запуск celery для windows в одном терминале
```sh
 python -m celery -A docker_hosting  worker --pool=solo -l info
 ```
4 Запуск сервера в другом терминале
```sh
manage.py migrate
manage.py instance_bd
python manage.py runserver
```
5 Выйти из виртуальной среды в любое время, просто введите 
```sh
 deactivate
```

## Актуальность
Наверное, самым известным в мире сервисом для размещения приложений в контейнерах является Heroku. 
Способ доставки через push в GIT. 

Альтернативой является российский сервис Amvera Cloud. Функционал аналогичен Хероку.

Существует панель управления игровым сервером Pterodactyl, который активно используется геймерами. 

Наш проект соединит стандартный хостинг с панелью управления. 


## Команда проекта
- [Владимир Недугов](https://github.com/Gorbacheb) — TeamLead Full-Stack Engineer
- [Анна Жукова](https://github.com/ann-zhukova) — Full-Stack Engineer
- [Алексей Панфилов](https://github.com/Zemlyanik1n) — Full-Stack Engineer
- [Михаил Юрин](https://github.com/Chuxan12) — Full-Stack Engineer
