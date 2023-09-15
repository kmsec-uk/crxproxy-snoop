FROM python:3.11-slim
WORKDIR /app/
COPY snoop.py requirements.txt /app/ 
RUN pip install -r /app/requirements.txt
CMD [ "python3", "/app/snoop.py"]