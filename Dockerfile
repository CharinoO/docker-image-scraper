FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/requirements.txt


RUN pip install -r /app/requirements.txt

EXPOSE 8501 

COPY ./ /app

ENTRYPOINT [ "streamlit", "run" ]

CMD ["main.py"]