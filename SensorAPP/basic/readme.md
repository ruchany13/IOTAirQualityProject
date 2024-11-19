- Build image and run. When run image humidity and temperature will be in output or use `-d` and look from logs.
```bash
docker build -t sensor-data-logger:1.0 .
docker run --privileged sensor-data-logger:1.0
```
