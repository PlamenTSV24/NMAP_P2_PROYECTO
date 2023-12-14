FROM python:3.9
RUN mkdir /web
WORKDIR /web
VOLUME ./web /web
COPY ./web /web
RUN pip install -r ./requirements.txt
CMD ["python3", "app.py"]