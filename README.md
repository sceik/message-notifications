
## Infrastruttura
Il progetto si compone di 3 elementi:
- Api: Web service per ricevere le notifiche
- RabbitMQ: usato per smistare le notifiche ai service
- Service: Servizio che si occupa di prendere i messaggi accodati e processarli

###Api
Espongono un servizio in ascolto sulla porta 5000, questo servizio espone la risorsa `/message`.

Tecnologia usata:

- [Flask](http://flask.pocoo.org/)
- [Swagger](http://swagger.io/)

###RabbitMQ
Immagine docker ufficiale docker di rabbitMQ. Una volta avviata e' disponibile all'indirizzo [http://localhost:15672/#/](http://localhost:15672/)
###Service
Contiene il servizio core che si occupa di interaggire con il Database.

Tecnologia usata:

- [Nameko](https://nameko.readthedocs.org)

## Get started
Require [docker-compose](https://docs.docker.com/compose/install/)

Per avviare l'applicazione eseguire: `docker-compose up`

Verranno avviati tre container docker ognuno con le compomenti sopra descritte.

Per testare l'applicazione e' possibile collegarsi a [http://127.0.0.1:5000/apidocs/]() ed seguire le richieste HTTP.
