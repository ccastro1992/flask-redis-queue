# Flask Redis Queue

Ejemplo para manejar un proceso en Flask mediante colas Redis, e implementado con Docker

### Quick Start

Spin up the containers:

```sh
$ docker-compose up -d --build
```

#### Levantar servicio Redis
```
sudo service redis-server status
```
#### Levantar dashboard procesos

```
rq-dashboard
```
#### Levantar worker para procesamiento de cola
```
python manage.py run_worker
```

Open your browser to http://localhost:5004
