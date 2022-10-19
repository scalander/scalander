FROM node:latest AS build
WORKDIR /usr/src/app
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
COPY . .
RUN npm run build
FROM node:latest
WORKDIR /app
ENV PORT 8080
ENV NODE_ENV=production
COPY --from=build /usr/src/app/build .
COPY --from=build /usr/src/app/package.json .
COPY --from=build /usr/src/app/package-lock.json .
RUN npm ci
ENV PORT 8080
EXPOSE 8080
RUN chown node /app
USER node
CMD ["node", "/app"]
