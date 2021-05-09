FROM frolvlad/alpine-miniconda3

WORKDIR /frontend
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y postgresql-client
RUN pip3 install -r requirements.txt

CMD ["psql < spotify-evaluation.sql"]
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "-p", "$PORT " ]