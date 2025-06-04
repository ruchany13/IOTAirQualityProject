- Run an influxdb image:
```bash
docker run -d -p 8086:8086 \      
    -e DOCKER_INFLUXDB_INIT_MODE=setup \
    -e DOCKER_INFLUXDB_INIT_USERNAME=my-user \   
    -e DOCKER_INFLUXDB_INIT_PASSWORD=my-password \    
    -e DOCKER_INFLUXDB_INIT_ORG=my-org \
    -e DOCKER_INFLUXDB_INIT_BUCKET=my-bucket \
    -e DOCKER_INFLUXDB_INIT_RETENTION=1w \
    -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token \
    influxdb:2
```
- Build image and run:
```bash
docker build -t sensor-data-logger:1.0-influxdb .
docker run --privileged \
    -e TOKEN=my-super-secret-auth-token \
    -e ORG=my-org \
    -e HOST='http://<server-ip>:8086' \
    -e BUCKET=my-bucket \
    rchyln/sensor-data-logger:1.0-influxdb
```