FROM python:3.8
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY modem_watchdog.py /
ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["./modem_watchdog.py"]
