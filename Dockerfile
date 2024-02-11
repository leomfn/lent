FROM python:3.11-alpine
EXPOSE 8000
WORKDIR /src
COPY requirements-prod.txt /src
RUN pip3 install -r requirements-prod.txt --no-cache-dir
COPY src /src
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
