#!/bin/bash

set -e


echo "Generating certificates..."

mkdir proxy/certs
mkdir -p proxy/htdocs/.well-known/acme-challenge

docker run --rm -d --name certbot-nginx   -p 80:80   -v "$(pwd)/proxy/htdocs:/usr/share/nginx/html:ro"   nginx

docker run --rm -it \
  -v "$(pwd)/proxy/certs:/etc/letsencrypt" \
  -v "$(pwd)/proxy/certs:/var/lib/letsencrypt" \
  -v "$(pwd)/proxy/htdocs:/usr/local/apache2/htdocs" \
  certbot/certbot certonly --webroot \
  --webroot-path /usr/local/apache2/htdocs \
  --email ciroautuori@outlook.it --agree-tos --non-interactive \
  -d solisoaps.it

docker run --rm -it \
  -v "$(pwd)/proxy/certs:/etc/letsencrypt" \
  -v "$(pwd)/proxy/certs:/var/lib/letsencrypt" \
  -v "$(pwd)/proxy/htdocs:/usr/local/apache2/htdocs" \
  certbot/certbot certonly --webroot \
  --webroot-path /usr/local/apache2/htdocs \
  --email ciroautuori@outlook.it --agree-tos --non-interactive \
  -d admin.solisoaps.it

docker stop certbot-nginx

echo "Certificate generated!"

STACK_NAME=soliso

echo "📦 Building backend image for the first time..."
docker build -t soliso-backend:latest ./backend

echo "📦 Building frontend image for the first time..."
docker build -t soliso-frontend:latest ./frontend

echo "📦 Building admin image for the first time..."
docker build -t soliso-admin:latest ./admin

echo "📦 Building proxy image for the first time..."
docker build -t soliso-proxy:latest ./proxy

echo "🐳 Creating stack..."
docker swarm init 
docker network create --driver overlay --attachable soliso-network
docker stack deploy -c docker-compose-prod.yaml ${STACK_NAME}
echo "✅ Stack created!"
