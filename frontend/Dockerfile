# ---------- BUILD STAGE ----------
FROM node:18-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install

# Copy env BEFORE build
COPY .env.production ./

COPY . .
RUN npm run build


# ---------- PRODUCTION STAGE ----------
FROM nginx:1.25-alpine

# Copy the built files
COPY --from=build /app/frontend_dist /usr/share/nginx/html

# Optional: custom nginx config (skip if not needed)

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
