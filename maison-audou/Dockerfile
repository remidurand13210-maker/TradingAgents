FROM node:22-bookworm-slim

WORKDIR /app

# Dépendances d'abord : le cache de couches survit aux changements de code.
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev

COPY src ./src
COPY public ./public
COPY scripts ./scripts

ENV NODE_ENV=production
ENV STORAGE_DIR=/coffre
ENV PORT=3000

# Le coffre est un volume : il doit survivre à la reconstruction de l'image.
VOLUME ["/coffre"]
EXPOSE 3000

CMD ["node", "src/server.js"]
