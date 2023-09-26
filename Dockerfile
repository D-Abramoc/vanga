FROM python:3.10-slim
RUN mkdir /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt --no-cache-dir
COPY vanga_back/ /app
WORKDIR /app
CMD [ "gunicorn", "vanga_back.wsgi:application", "--bind", "0:8000" ]