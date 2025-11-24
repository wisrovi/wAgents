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
	docker-compose up -d --build
	docker push wisrovi/agents:gpu-slim

# Bajar el contenedor
stop:
	docker-compose down

# Entrar al contenedor (sesión interactiva)
into:
	docker-compose exec agent zsh

# Ver logs
logs:
	docker-compose logs -f agent
