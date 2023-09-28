# vanga

![Workflow for test, build and deploy](https://github.com/D-Abramoc/vanga/actions/workflows/vanga_cicd.yml/badge.svg)

# Предсказывает продажи, сокращает издержки
## Команда разработчиков
## Запуск приложения ##
- клонировать репозиторий
```
git clone git@github.com:D-Abramoc/vanga.git
```
- создать окружение
- установить зависимости
```
pip install -r requirements.txt
```
- создать файл .env заполнить по примеру env.sample
## Импорт базы данных ##
- первичный импорт осуществляется автоматически при развертывании контейнеров
- для импорта данных о продажах:
1) скопировать .csv файл с данными в папку /data
2) выполнить команду:
```
python manage.py import_sales filename.csv
```
- filename.csv - имя файла с указанием формата