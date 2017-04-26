FROM python:3
ADD api.py /app/
WORKDIR /app
RUN pip install nameko
RUN pip install flask
RUN pip install flasgger

CMD [ "python", "./api.py" ]