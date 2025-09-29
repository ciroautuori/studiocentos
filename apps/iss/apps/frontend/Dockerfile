# Frontend Dockerfile for ISS - Innovazione Sociale Salernitana
# Multi-stage build ottimizzato per produzione

# Build stage
FROM node:20-alpine AS builder

# Installa dipendenze di sistema per build
RUN apk add --no-cache git python3 make g++

# Installa pnpm globalmente
RUN corepack enable && corepack prepare pnpm@9.0.0 --activate

# Set working directory
WORKDIR /app

# Copia solo i file di configurazione per cache layer
COPY package.json pnpm-lock.yaml* ./
COPY tsconfig.json tsconfig.node.json vite.config.ts tailwind.config.ts postcss.config.js ./

# Installa dipendenze (layer cacheable)
RUN pnpm install --frozen-lockfile --prefer-offline

# Copia il codice sorgente
COPY src/ ./src/
COPY public/ ./public/
COPY index.html ./

# Build ottimizzato per produzione
ENV NODE_ENV=production
ENV VITE_API_BASE_URL=/api
RUN pnpm build && \
    # Rimuovi source maps per sicurezza
    find dist -name "*.map" -delete && \
    # Comprimi ulteriormente i file
    find dist -name "*.js" -exec gzip -k {} \; && \
    find dist -name "*.css" -exec gzip -k {} \;

# Production stage - Nginx ottimizzato
FROM nginx:1.25-alpine AS production

# Installa curl per health checks
RUN apk add --no-cache curl

# Rimuovi configurazione nginx default
RUN rm /etc/nginx/conf.d/default.conf

# Copia configurazione nginx ottimizzata
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia applicazione builddata dal builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Ottimizza permessi
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Crea directory per logs e cache
RUN mkdir -p /var/log/nginx /var/cache/nginx/client_temp /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp /var/cache/nginx/uwsgi_temp /var/cache/nginx/scgi_temp && \
    touch /var/log/nginx/access.log /var/log/nginx/error.log && \
    chown -R nginx:nginx /var/log/nginx /var/cache/nginx && \
    chmod -R 755 /var/cache/nginx

# Health check ottimizzato
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:80/ || exit 1

# Esponi porta
EXPOSE 80

# Start nginx (rimuoviamo USER nginx per evitare problemi di permessi)
CMD ["nginx", "-g", "daemon off;"]
