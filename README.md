<h1 align="center">Social network with simple REST API</h1>
Тестовое задание социальной сети.

## Технологии:
### Djando, Django REST frameworks, PostgreSQL, Docker (docker-compose)

## Требования:
<p>Реализовать REST API для социальной сети.</p>
<p>Базовые модели:</p>
<ul>
    <li>User</li>
    <li>Post (всегда созданные пользователем)</li>
</ul>
<p>Базовые особенности:</p>
<ul>
    <li>регистрация пользователя</li>
    <li>аутентификация пользователя по токенам (JWT предпочтительней)</li>
    <li>создание поста</li>
    <li>поставить лайк на пост</li>
    <li>убрать лайк с поста</li>
</ul>

### Примечание:
Аттрибуты для объектов User и Post на усмотрение разработчика.

<h2 align="center">Запуск приложения</h2>
После клонирования проекта для корректной работы необходимо создать
файлы `.env` и `.env.db` в корневой папке следующего содержания:
1. `.env`

```
DEBUG=1
SECRET_KEY=СЮДА_ВСТАВИТЬ_ВАШ_СЕКРЕТНЫЙ_DJANGO_КЛЮЧ
ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
DATABASE_URL=psql://social_network_user:password@db:5432/social_network_db
```

2. `.env.db`

```
POSTGRES_USER=social_network_user
POSTGRES_PASSWORD=password
POSTGRES_DB=social_network_db
```

Для запуска проекта перейдите в корень проекта и выполните команду:
3. `docker-compose up -d`

Для создания superuser выполните команду:
4. `docker-compose exec web python manage.py createsuperuser`

Посты и пользователей можно создать через админ-панель по адресу
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) или через API запросы согласно документации ниже.

<h2 align="center">API документация</h2>

### Доступные API методы для пользователей:
**POST** `api/signup/` - регистрация пользователя <br>
**POST** `api/jwt/login/` - получение JWT путем отправки username и password пользователя

### Доступные API методы для постов:
**GET, POST** `api/v1/post/` - Получение списка всех постов и создание нового <br>
**GET, PATCH** `api/v1/post/<id>/` - Получение информации о посте и изменение конкретного поля поста <br>
**PATCH** `api/v1/post/<id>/like/` - Добавление и удаление лайка на пост от текущего пользователя <br>
