FROM python:3.8
COPY requirements.txt /
COPY modem_watchdog.py /
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["./modem_watchdog.py"]
