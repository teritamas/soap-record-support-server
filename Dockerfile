FROM python:3.10-slim-buster

ENV LC_ALL C.UTF-8
ENV HOME /app

WORKDIR $HOME
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./ .

CMD ["python" ,"main.py"]