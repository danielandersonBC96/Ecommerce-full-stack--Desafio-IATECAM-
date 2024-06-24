# Stage 1: Build the Angular app
FROM node:18 AS build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Clean NPM cache
RUN npm cache clean --force

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Run the build command with the correct configuration flag
RUN npm run build

# Stage 2: Setup NGINX to serve the Angular app
FROM nginx:alpine

# Copy the built Angular app from the build stage
COPY --from=build /app/dist/nome-do-projeto /usr/share/nginx/html

# Copy the NGINX configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
