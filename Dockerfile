FROM python:3.6.5

WORKDIR /usr/src/app

COPY Pipfile ./
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install

COPY . .

CMD [ "pipenv", "run", "python", "./main.py" ]
