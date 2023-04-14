FROM python:3.9-slim as compiler
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt

FROM python:3.9-slim as runner
WORKDIR /app/
COPY --from=compiler /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /app/
CMD ["python", "app.py", ]


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
