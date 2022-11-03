FROM node:latest 
WORKDIR /usr/src/app
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
RUN npm ci
COPY . .
RUN npm run build
RUN npm ci
ENV PORT 8080
EXPOSE 8080
CMD ["node", "."]
