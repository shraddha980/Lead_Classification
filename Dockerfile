FROM python:3.8
USER root
RUN mkdir /app
COPY . /app/
WORKDIR /app/
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
ENV AIRFLOW_HOME = "/app/airflow"
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT = 1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING = True
ENV SQLALCHEMY_WARN_20 = 1
ENV SQLALCHEMY_SILENCE_UBER_WARNING = 1
RUN airflow db init
RUN airflow users create -e shraddhawork45@gmail.com -f Shraddha -l Sawant -p admin -r Admin -u admin
RUN chmod 777 start.sh
RUN apt update -y && apt install awscli -y
ENTRYPOINT ["/bin/sh"]
CMD ["start.sh"]
