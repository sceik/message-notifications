import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@rabbit"}

@app.before_request
def log_request_info():
    logging.info('=INFO REPORT==== Headers: %s', request.headers)
    logging.info('=INFO REPORT==== Body: %s', request.get_data())

@app.route('/message', methods=['POST'])
def message():
    """
    Micro Service Based Message API
    This API is made with Flask, Flasgger and Nameko
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: data
          properties:
            message:
              type: string
    responses:
      200:
        description: Your message has been recived
    """
    message = request.json.get('message')
    msg = "Your message has been recived"
    with ClusterRpcProxy(CONFIG) as rpc:
        # asynchronously spawning the message compute task
        rpc.message.message.async(message)
        return msg, 200

if __name__ == '__main__':
    logging.basicConfig(filename='api.log',level=logging.DEBUG)
    # logging.basicConfig(filename='api.log',level=logging.DEBUG)
    # handler = RotatingFileHandler('api.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # handler.setLevel(logging.ERROR)
    # handler.setLevel(logging.WARNING)
    # app.logger.addHandler(handler)
    app.run(debug=True,host='0.0.0.0')