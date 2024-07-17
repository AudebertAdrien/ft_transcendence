.PHONY: all build down clean logs

all: build
	@echo "Building Docker images..."
	sudo mkdir -p $$PWD/data/db
	sudo docker compose -f ./docker-compose.yaml up -d --build

down:
	@echo "Stopping Docker containers..."
	sudo docker compose -f ./docker-compose.yaml down

clean:
	@echo "Cleaning up Docker resources..."
	sudo docker stop $$(docker ps -qa);\
    sudo docker rm $$(docker ps -qa);\
    sudo docker rmi $$(docker image ls -q);\
    sudo docker volume rm $$(docker volume ls -q);\
	sudo rm -rf $$PWd/data/db ;\

logs:
	@echo "Displaying Docker logs..."
	sudo docker compose logs -f

re:	down clean build 
