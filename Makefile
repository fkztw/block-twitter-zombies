docker_build:
	docker build -t block-twitter-zombies .

docker_run:
	docker run -it --mount src=`pwd`,target=/usr/src/app,type=bind block-twitter-zombies:latest
