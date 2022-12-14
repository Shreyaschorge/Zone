FROM sanicframework/sanic:3.8-latest

WORKDIR /sanic

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["python", "src/index.py"]