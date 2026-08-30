# ==============================================================================
# GovFlow Frontend (Next.js 14 / React 18) Dockerfile
# ==============================================================================
FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=development \
    PORT=3000

# Install dependencies from root package.json and apps/web package.json
COPY package.json ./package.json
COPY apps/web/package.json ./apps/web/package.json
COPY packages/shared-types/package.json ./packages/shared-types/package.json
COPY packages/api-contracts/package.json ./packages/api-contracts/package.json
COPY packages/ui-kit/package.json ./packages/ui-kit/package.json
COPY packages/config/package.json ./packages/config/package.json

WORKDIR /app/apps/web
RUN npm install

WORKDIR /app
COPY packages/ ./packages/
COPY apps/web/ ./apps/web/

WORKDIR /app/apps/web

EXPOSE 3000

CMD ["npm", "run", "dev"]