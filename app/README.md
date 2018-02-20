

# application code

## starting the app

This section contains details on starting up the application. For now, we are using `docker-compose` for orchestration, just to speed up development.

To rebuild any service containers:

```
docker-compose build
```

Kick up the app:

```
docker-compose up -d
```

Then check it out on `localhost:5090` in your browser.

Whenever you're done, shut down the app:

```
docker-compose down
```

## references

- https://github.com/juggernaut/nginx-flask-postgres-docker-compose-example