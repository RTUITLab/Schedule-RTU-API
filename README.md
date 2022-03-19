# Schedule-RTU

API for getting a schedule of RTU MIREA.

# Build service from Docker image
Requirements:
* Docker

## Run container:

Clone or download this repo and create .env with database URI that should be used for the connection to database. 
```
DATABASE_URL=dialect+driver://username:password@host:port/database
ROOT_PATH=# path prefix to service from proxy
APP_SECRET=# token for access to protected roots

```

Build container 
* ```docker build -t schedule-rtu:latest .```

Run container
* ```docker run -it -p 8000:8000 schedule-rtu:latest```

App running on ```http://0.0.0.0:8000/```

You can find api on ```http://localhost:8000/docs/ ```

## Deploy

Run next command to generate swarm stack file
```bash
# bash
docker-compose -f docker-compose.yml -f docker-compose.production.yml config | sed "s/[0-9]\+\.[0-9]\+$/'\0'/g" >| stack.yml
```
## Contributing
You are welcome to contribute whatever you think will be helpful for the project. Feel free to create an issue or submit a pull request and we can discuss further.

Special thanks to [YaSlavar](https://github.com/YaSlavar) with [parser_mirea](https://github.com/YaSlavar/parser_mirea). This project was very helpful at the beginning of the development.