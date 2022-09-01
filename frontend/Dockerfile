FROM node:lts-alpine AS build
ENV NODE_ENV=production
WORKDIR /usr/src/app
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
ENV PORT 8080
RUN npm install --production --silent && mv node_modules ../
COPY . .
RUN npm run build
EXPOSE 8080
RUN chown -R node /usr/src/app
USER node
CMD ["node", "build"]
