### 介绍

一个简易的线上粘贴板。

### 技术栈
采用前后端分离的方式  
前端：Vue + nginx  
后端：Flask + uWSGI

### 部署
```shell
docker-compose pull  # 若想要在本地build，则无需执行本行
docker-compose up -d
```
服务启动后，在浏览器打开`http://localhost:8080`即可使用。  
默认将前端服务部署在8080端口，有需要可自行到`docker-compose.yml`进行修改。  
后端容器虽然对外暴露了端口，但实际上接口的调用是通过前端容器里的nginx进行了内部转发，浏览器并不会跟后端容器直接进行通信。  
根据自身需求，你可以选择将前后端分别独立部署，目录下分别有对应的Dockerfile可以使用。
