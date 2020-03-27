# flask-docker-api
This is a basic flask API running in a docker container.

To run this basic API - first install docker
https://www.docker.com/

Next, in the root directory run the following command in a bash console - `bash start.sh` 
This will build and run the image on port 56733:80

You can reload change by using the command `touch uwsgi.ini` 

You can view the endpoints available by going to localhost:56733/site-map
