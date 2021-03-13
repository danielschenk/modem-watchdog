FROM python:3.8-alpine
COPY requirements.txt /
COPY modem_watchdog.py /
RUN pip install -r requirements.txt

ENTRYPOINT ["./modem_watchdog.py"]