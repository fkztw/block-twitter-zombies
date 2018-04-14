docker_build:
	docker build -t block-twitter-zombies .

docker_run:
	docker run -it -v `pwd`:/usr/src/app block-twitter-zombies:latest
