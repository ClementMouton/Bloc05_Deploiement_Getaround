FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y


RUN pip install pandas streamlit scikit-learn plotly numpy openpyxl uvicorn statsmodels

COPY . /home/app

# CMD streamlit run --server.port $PORT app.py

# Exposer le port sur lequel l'application Streamlit sera accessible
EXPOSE 8501

# Définir la commande pour lancer l'application Streamlit
CMD ["streamlit", "run", "app.py"]