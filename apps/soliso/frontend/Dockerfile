# Fase di build
FROM node:23.11.0-slim AS builder

WORKDIR /app

# Copia i file delle dipendenze
COPY package*.json ./

# Installa le dipendenze
RUN npm install

# Copia tutto il codice sorgente
COPY . .

# Builda l'applicazione Vue.js
RUN npm run build

# Fase di produzione con Nginx
FROM nginx:stable-alpine

# Rimuove la configurazione di default di Nginx
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copia la configurazione personalizzata di Nginx
COPY nginx.conf /etc/nginx/conf.d

# Copia i file buildati dalla fase precedente
COPY --from=builder /app/dist /usr/share/nginx/html

# Avvia Nginx
CMD ["nginx", "-g", "daemon off;"]
