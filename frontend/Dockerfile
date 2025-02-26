# Base image
FROM node:23.8.0-alpine3.20

# Set working directory
WORKDIR /watchman

# Copy package.json and package-lock.json (or yarn.lock)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --production

# Copy compiled Next.js build files
COPY .next .next
COPY public public
COPY next.config.ts next.config.ts

# Expose the port Next.js runs on
EXPOSE 3500

# Start the Next.js server
CMD ["npm", "run", "start"]
