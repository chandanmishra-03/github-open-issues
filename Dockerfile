#getting a base image
FROM python:3.6-jessie
#making workdir
WORKDIR /app
#copying items to workdir
COPY ./app /app
#installing all requiremet packages
RUN pip install --no-cache-dir -r requirements.txt
#running app using gunicorn
CMD ["gunicorn", "app:app", "--config=config.py"]
