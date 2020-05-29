# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install --registry=https://registry.npm.taobao.org
COPY . .
ARG VUE_APP_API_HOST
RUN npm run build

# production server
FROM nginx:stable-alpine as production-server
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
# VOLUME [ "/etc/nginx/nginx.conf" ]
CMD ["nginx", "-g", "daemon off;"]


# 仅用于生成静态文件，通过挂载形式获取
FROM alpine:latest as production-dist
RUN mkdir /tmp/dist
COPY --from=build-stage /app/dist /tmp/dist
VOLUME [ "/app/dist" ]
ENTRYPOINT ["cp", "-r", "/tmp/dist", "/app/dist/"]