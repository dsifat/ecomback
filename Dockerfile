FROM python:3.8.4

COPY . code
WORKDIR code

RUN pip install -r requirements.txt
EXPOSE 9000
#CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]