FROM python:3.8

EXPOSE 8000

WORKDIR /InternshipBot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]