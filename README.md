# YaMDb 

## Описание:

API проекта YaMDb - сервиса по сбору отзывов и оценок на различные кинофильмы, музыкальные и литературные произведения с возможностью оставлять комментарии к пользовательским рецензиям.

### Запуск проекта:

*Клонируем репозиторий и переходим в него в командной строке:*

``` git clone git@github.com:ivnpvl/api_yamdb.git ```

``` cd api_yamdb ```

*Cоздаем и активируем виртуальное окружение:*

``` python -m venv venv ```

``` source venv/scripts/activate ``` (для Windows) 

``` source env/bin/activate ``` (для Linux/Mac) 

*Устанавливаем зависимости из файла requirements.txt:*

``` python -m pip install --upgrade pip ```

``` pip install -r requirements.txt ```

*Выполняем миграции:*

``` python manage.py migrate ```

*Загружаем информацию из csv-файлов в базу данных:*

``` python manage.py import_csv_data ```

*Запускаем сервер:*

``` python manage.py runserver ```

### Аутентификация:

Для регистрации отправляем POST-запрос на адрес ``` http://127.0.0.1:8000/api/v1/auth/signup/ ```, передав почту и имя пользователя в тело запроса.

После этого на почту приходит код подтверждения, который отправляем на адрес ``` http://127.0.0.1:8000/api/v1/auth/token/ ```, передав код подтверждения и имя пользователя в тело запроса.

В ответ на запрос приходит токен. После получения токена передаем его в заголовке ``` Authorization: Bearer Token ``` при отправке запросов.

Пользуемся сервисом.

### Примеры запросов:

Регистрация нового пользователя: ``` http://127.0.0.1:8000/api/v1/auth/signup/ ```

POST-запрос на этот адрес:

```
{
"email": "user@example.com",
"username": "string"
}
```
Ответ:
```
{
"email": "string",
"username": "string"
}
```
Список жанров: ``` http://127.0.0.1:8000/api/v1/genres/ ```

GET-запрос на этот адрес вернет:

```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"name": "string",
"slug": "string"
}
]
}
```

Остальная документация по API:  ``` http://127.0.0.1:8000/redoc/ ```
