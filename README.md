# django-pokemon-api

# django-pokemon-api

Este proyecto es una aplicación web desarrollada con Django. En este documento, encontrarás las instrucciones detalladas para levantar el proyecto usando Docker Compose, además de cómo realizar pruebas y ejecutar comandos de Django en un entorno local.

## Requisitos
Antes de proceder, asegúrate de tener instalados los siguientes programas en tu sistema:

- **Docker:** Una plataforma de contenedores que permite simplificar la configuración y despliegue de aplicaciones. Instala Docker desde [aquí](https://www.docker.com/get-started).
- **Docker Compose:** Una herramienta para definir y ejecutar aplicaciones Docker multi-contenedor. Viene incluido en las instalaciones de Docker Desktop para Windows y Mac, pero en Linux podrías necesitar instalarlo aparte desde [aquí](https://docs.docker.com/compose/install/).

Verifica la instalación con los siguientes comandos:

```bash
docker --version
docker-compose --version
```

## Ejecutar la Applicacion de django con docker-compose

```
docker-compose build
docker-compose up -d
```
 Para ver los logs de la aplicación 
````
docker-compose logs -f
```


