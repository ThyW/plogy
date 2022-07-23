from alpine:latest

ENV PYTHONUNBUFFERED=1

RUN apk add --update --no-cache python3 \
    && apk add --no-cache sqlite \
    && ln -sf python3 /usr/bin/python \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip \
    && pip3 install --no-cache --upgrade pip setuptools 

WORKDIR /flaskapp

COPY . /flaskapp

RUN python -m pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["src/main.py"]
