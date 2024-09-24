FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y

RUN curl -fsSL https://get.deta.dev/cli.sh | sh
RUN pip install fastapi boto3 "uvicorn[standard]" pydantic jinja2 pandas gunicorn joblib openpyxl scikit-learn xgboost
RUN export FLASK_APP=api
COPY . /home/app

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "4000"]