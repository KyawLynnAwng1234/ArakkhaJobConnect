# ---------- BUILD STAGE ----------
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

# Copy env and rename to .env so Vite loads it
COPY .env.production ./.env

# Copy the rest
COPY . .
RUN npm run build

# ---------- PRODUCTION STAGE ----------
FROM nginx:1.25-alpine

# Copy compiled frontend
COPY --from=build /app/frontend_dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
