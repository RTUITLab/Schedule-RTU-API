# Schedule-RTU

[![Build Status](https://dev.azure.com/rtuitlab/RTU%20IT%20Lab/_apis/build/status/Schedule-RTU-API?branchName=master)](https://dev.azure.com/rtuitlab/RTU%20IT%20Lab/_build/latest?definitionId=159&branchName=master)

Service for getting jsons with a schedule for a given group of RTU MIREA

# Build service from Docker image
Requirements:
* Docker

## Run container:

Clone or download this repo and build container 
* ```docker build -t schedule-rtu:latest .```

Run container
* ```docker run -it -p 5000:5000 schedule-rtu:latest```

App running on ```http://0.0.0.0:5000/```

You can find api on ```http://localhost:5000/api/schedule/docs/ ```

## Deploy

Run next command to generate swarm stack file
```bash
# bash
docker-compose -f docker-compose.yml -f docker-compose.production.yml config | sed "s/[0-9]\+\.[0-9]\+$/'\0'/g" >| stack.yml
```
## Contributing
You are welcome to contribute whatever you think will be helpful for the project. Feel free to create an issue or submit a pull request and we can discuss further.

Special thanks to [YaSlavar](https://github.com/YaSlavar) with [parser_mirea](https://github.com/YaSlavar/parser_mirea). This project was very helpful at the beginning of the development.