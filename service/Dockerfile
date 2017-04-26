FROM python:3
COPY . /service/
WORKDIR /service
RUN pip install nameko

CMD nameko run --config ./serviceConfig.yaml service --broker amqp://guest:guest@rabbit