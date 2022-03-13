FROM python:3.10.2-slim-buster

COPY ./requirements.txt /app/requirements.txt


RUN pip3 install -r app/requirements.txt

############################

WORKDIR /app

COPY ./ /app/

RUN mkdir Data-Tokopedia Data-Shopee

EXPOSE 8501

CMD [ "streamlit", "run" , "main.py", "--server.headless=true"]
