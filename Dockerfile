FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

copy . /app

CMD ["flask", "run" , "--host", "0.0.0.0", "--port", "5000"]