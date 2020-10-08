FROM python:3.8.5

WORKDIR /usr/src/app

COPY Pipfile .
COPY Pipfile.lock .

RUN python -m pip install --upgrade pip \
    && pip install pipenv install \
    && pipenv install --deploy --system

COPY . .

EXPOSE 8080

ENTRYPOINT ["uvicorn"]

CMD ["url_shortener.app:app", "--host", "0.0.0.0", "--port", "8080"]
