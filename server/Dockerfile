FROM python:3.8-slim-buster
# FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

#RUN apk update \
#  && apk add --virtual build-deps gcc python3-dev musl-dev \
#  && apk add postgresql-dev \
#  # Pillow dependencies
#  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
#  # CFFI dependencies
#  && apk add libffi-dev openssl-dev py-cffi \
#  # Translations dependencies
#  && apk add gettext \
#  && apk add cargo

ADD . .

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./scripts/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./scripts/server.sh /server.sh
RUN sed -i 's/\r//' /server.sh
RUN chmod +x /server.sh

COPY ./scripts/worker.sh /worker.sh
RUN sed -i 's/\r//' /worker.sh
RUN chmod +x /worker.sh

COPY ./scripts/beat.sh /beat.sh
RUN sed -i 's/\r//' /beat.sh
RUN chmod +x /beat.sh

WORKDIR /

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
