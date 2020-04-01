# flask-docker-api
This is a basic flask API running in a docker container.

To run this basic API - first install docker
https://www.docker.com/

Next, in the root project directory run the following command in console `docker-compose up -d --build` this will create a default network for the app, install all dependencies and run the redis, celery, and flask containersm this runs in detatched mode. To stop use `docker-compose down` and to restart `docker-compose up` You do not need to rebuild the containers every time. You can without the `-d` flag to not run in detatched mode.

You can then go to localhost:5000 to view the flask app, and localhost:5555 to view flower to monitor the workers that run background tasks.

Hot reloading is enabled by via the Dockerfile running the flask app in debug mode

You can view the endpoints available by going to localhost:5000/site-map

