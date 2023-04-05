# Simple project with RabbitMQ

## Launch
- git clone https://github.com/evgenchikk/rabbitmq-sample-project

- run "docker compose up -d"<br>
App will start on port 3000

## HTTP methods:
#### POST /image
Requires a file upload<br>
This method just uploads your image<br><br>
___curl example:___<br>
curl -X POST -F "file=@\<path to your file\>" localhost:3000/image

#### POST /image/{id}
Requires a request body<br>
This methoad allows to do resize or grayscaling uploaded images<br><br>
___curl example for grayscale:___<br>
curl -X POST -d '{"action": "grayscale"}' localhost:3000/image/2<br><br>
___curl example for resizing:___<br>
curl -X POST -d '{"action": "resize 200,200"}' localhost:3000/image/2<br>

#### GET /image/{id}
This method downloads modified image<br><br>
___curl exmaple:___<br>
curl -X GET -O -J localhost:3000/image/2
