# -------------------------------------
# 1️⃣ Build Stage (Vite Production Build)
# -------------------------------------
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and lock file
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all frontend source code
COPY . .

# Build Vite production files
RUN npm run build



# -------------------------------------
# 2️⃣ NGINX Stage (Serve Static Files)
# -------------------------------------
FROM nginx:1.25-alpine

# Copy build output to nginx public folder
COPY --from=build /app/frontend_dist /usr/share/nginx/html

# Replace default nginx config (optional but recommended)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
