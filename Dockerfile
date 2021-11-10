FROM python:3.8
ENV PORT=8000
COPY . /var/www
WORKDIR /var/www
RUN apt update && apt upgrade -y && apt clean -y && apt autoclean -y && apt autoremove -y && apt install ffmpeg -y
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
ENTRYPOINT python manage.py runserver 0:${PORT}
EXPOSE ${PORT}