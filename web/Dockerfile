FROM python:3.7

WORKDIR /usr/local/dash

RUN pip install pandas
RUN pip install dash==0.43.0
RUN pip install dash-daq==0.1.0

ENTRYPOINT [ "python", "./app/app.py" ]
