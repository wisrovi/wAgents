.PHONY: fix-inotify build up down exec logs

# Arreglar límite de inotify para que funcione dijo
fix-inotify:
	@echo "Aumentando el límite de inotify en el host..."
	echo fs.inotify.max_user_instances=512 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p

# Construir la imagen
build:
	docker-compose build

# Levantar el contenedor
start:
	docker-compose up agent -d --build
	docker-compose up dvc -d --build
	docker-compose up yolo -d --build
	docker-compose up complete -d --build
	docker-compose down
	docker push wisrovi/agents:gpu-slim
	docker push wisrovi/agents:gpu-slim-dvc
	docker push wisrovi/agents:gpu-slim-yolo
	docker push wisrovi/agents:gpu

# Bajar el contenedor
stop:
	docker-compose down

# Entrar al contenedor (sesión interactiva)
into:
	docker-compose exec agent zsh

# Ver logs
logs:
	docker-compose logs -f agent
