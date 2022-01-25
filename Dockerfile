FROM python:3.9

WORKDIR 'usr/src/app'

COPY ./requirments.txt ./

RUN pip install -r requirments.txt

COPY ./ ./

CMD ['python', 'main.py']

