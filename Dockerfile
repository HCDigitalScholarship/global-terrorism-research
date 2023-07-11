FROM python:2.7.13-stretch

WORKDIR /app
ENV DJANGO_SETTINGS_MODULE=gtr.settings_docker

RUN pip install setuptools_scm

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

RUN SECRET_KEY=1 python manage.py collectstatic --noinput

EXPOSE 8000

CMD /app/docker-entrypoint.sh