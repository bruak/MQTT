FROM python:3.10-slim
WORKDIR /app
COPY subscriber.py .
RUN pip install paho-mqtt requests datetime pytz
CMD ["python", "subscriber.py"]
