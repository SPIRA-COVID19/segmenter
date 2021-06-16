FROM python:3.9

RUN pip install pipenv

RUN apt-get update && apt-get install -y libsndfile1

WORKDIR /segmenter

COPY Pipfile Pipfile.lock ./

RUN pipenv sync

COPY . .

ENTRYPOINT ["pipenv", "run", "python", "main.py"]