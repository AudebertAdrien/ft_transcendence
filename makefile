MAIN_PROJECT_NAME=main_project
ELK_PROJECT_NAME=elk_project

COMPOSE_FILE=docker-compose.yml
ELK_COMPOSE_FILE=docker-compose-elk.yml

COMPOSE=docker compose -f $(COMPOSE_FILE) -p $(MAIN_PROJECT_NAME)
ELK_COMPOSE=docker compose -f $(ELK_COMPOSE_FILE) -p $(ELK_PROJECT_NAME)

CONTAINER=$(c)

up: down
	$(COMPOSE) build
	$(COMPOSE) up -d $(CONTAINER) || true

build:
	$(COMPOSE) build $(CONTAINER)

down:
	$(COMPOSE) down $(CONTAINER)

destroy:
	$(COMPOSE) down -v --rmi all

ssl-certs:
	openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
    -keyout certs/ssl/private.key -out certs/ssl/certificate.crt \
    -config config/ssl.conf

# Manage ELK stack

elk-up:
	$(ELK_COMPOSE) up -d --remove-orphans || true

elk-down:
	$(ELK_COMPOSE) down --remove-orphans 

elk-destroy:
	$(ELK_COMPOSE) down --remove-orphans  -v --rmi all

kill-pid:
	sudo lsof -i :5432 | awk 'NR>1 {print $$2}' | xargs sudo kill -9 || true
	sudo lsof -i :5601 | awk 'NR>1 {print $$2}' | xargs sudo kill -9 || true
	sudo lsof -i :9200 | awk 'NR>1 {print $$2}' | xargs sudo kill -9 || true
	sudo lsof -i :8080 | awk 'NR>1 {print $$2}' | xargs sudo kill -9 || true
	sudo lsof -i :5044 | awk 'NR>1 {print $$2}' | xargs sudo kill -9 || true

db-shell:
	$(COMPOSE) exec db psql -U 42student players_db 

help:
	@echo "Usage:"
	@echo "  make build [c=service]        # Build images"
	@echo "  make up [c=service]           # Start containers in detached mode"
	@echo "  make start [c=service]        # Start existing containers"
	@echo "  make down [c=service]         # Stop and remove containers"
	@echo "  make destroy				   # Stop and remove containers and volumes"
	@echo "  make stop [c=service]         # Stop containers"
	@echo "  make logs [c=service]         # Tail logs of containers"
	@echo "  make ssl-certs                # create ssl certificate"
	@echo "  make help                     # Show this help"

.PHONY: up build start stop down destroy logs ps db-shell help

