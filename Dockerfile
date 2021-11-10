FROM python:3.8
ENV PORT=8000
ENV PYTHONUNBUFFERED=1
WORKDIR /var/www
COPY requirements.txt /var/www
RUN apt update && apt upgrade -y && apt clean -y && apt autoclean -y && apt autoremove -y && apt install ffmpeg libmysqld-dev default-mysql-client -y
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt