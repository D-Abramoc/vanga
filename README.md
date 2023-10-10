# Lenta-Yandex Hackathon September 2023

![Workflow for test, build and deploy](https://github.com/D-Abramoc/vanga/actions/workflows/vanga_cicd.yml/badge.svg)

# Предсказывает продажи, сокращает издержки
## Команда разработчиков
- PM: Анастасия Шувалова [instagram](https://instagram.com/emma_evans9)
- DS: Ярослав Князев [github](https://github.com/Yaroslav-Kn)
- DS: Янис Пайст [github](https://github.com/IanisPaist)
- DS: Евгений Мусаев
- Design: Эльвира Рассолова [behance](https://www.behance.net/b3b2f015)
- Design: Ольга Новожилова [behance](https://www.behance.net/novozhilova)
- Frontend: Антон Лысцов [github](https://github.com/777toha)
- Frontend: Андрей Симонов [github](https://github.com/2web)
- Backend: Дмитрий Абрамов [github](https://github.com/D-Abramoc)
- Backend: Андрей Ядин [github](https://github.com/aayadin)
## Проект доступен по url:

[http://158.160.123.145](http://158.160.123.145)

## Запуск приложения ##
- клонировать репозиторий
```
git clone git@github.com:D-Abramoc/vanga.git
```
- создать файл .env заполнить по примеру env.sample
- из папки с файлом docker-compose.yml выполнить команду:
```
docker-compose up
```
- После развертывания проекта применить миграции:
```
docker-compose exec -T web python manage.py migrate
```
- Подключить статические файлы:
```
docker-compose exec -T web python manage.py collectstatic --no-input
```
### Импорт базы данных ###
- для базы данных (без продаж) выполнить команду:
```
docker-compose exec -T web python manage.py import_db
```
- импорт данных о продажах (занимает продолжительное время, в зависимости от произвеодительности оборудования 25-45 минут):
```
docker-compose exec -T web python manage.py import_sales sales_df_train.csv false
```
- Импорт новых данных о продажах возможен через интерфейс сайта, а также с помощью вышеописанной команды. Потребуется разместить файл в формате .csv в папке vanga_back/data, в качестве параметров передать в команду имя этого файла и параметр "true", который позволит передать загруженные данные на сервер DS для получения прогноза:
```
docker-compose exec -T web python manage.py import_sales new_sales.csv true
```
### Документация по API будет доступна по ссылке ###
```
http://localhost/api/docs
```
## Описание работы ресурса ##

- /vanga_back: директория backend
- /vanga_ds: директория data science
- /dist: директория frontend

В части Backend реализованы 4 приложения:
- backend - основные модели и команды управления
- api - взаимодействие с Frontend
- forecast - взаимодействие с DS
- users - управление пользователями, авторизация

1) После поступления новых данных о продажах они сохраняются в базу и отправляются на сервер DataScience для расчета прогноза;
2) Сервер Django после таймаута запрос на отправку прогноза, и после получения данных сохраняет их в базу;
3) Данные доступны для просмотра и анализа через клиентскую часть;

## Используемые технологии ##
- Python
- [Django] (https://www.djangoproject.com/)
- [Django REST Framework] (https://www.django-rest-framework.org/)
- [Pandas] (https://pandas.pydata.org/)
- [Docker] (https://www.docker.com/)
- [Nginx] (https://nginx.org/ru/)
- [PostgresQL] (https://www.postgresql.org/)
- [Gunicorn] (https://gunicorn.org/)
