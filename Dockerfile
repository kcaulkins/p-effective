FROM python:3

ADD .env /

ADD requirements.txt /
RUN pip install -r requirements.txt

ADD bot.py /

CMD [ "python", "./bot.py" ]