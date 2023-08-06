# Project Name

## Requirement


## Start

```bash
python -m servers.model.main
python -m servers.web.main (OR gunicorn -c servers/web/gunicorn_config.py servers.web.main:app)
```

## Deploy

- `cd deploy`
- `./build_image.sh 0.x` (0.x is the version of your Docker image version)
- `kubectl apply -f kubernetes.yaml`