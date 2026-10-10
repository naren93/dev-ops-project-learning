## HelloWorldApi

Minimal .NET 8 API intended to be built and run entirely with Docker.

### Build

```bash
cd HelloWorldApi
docker build -t hello-world-api:v1 .
```

### Run

```bash
docker run --rm -p 8080:8080 hello-world-api:v1
```

Test it at `http://localhost:8080/` and `http://localhost:8080/health`.

### Rebuild and redeploy

The idempotent script rebuilds the image, tags it as `v1` and `latest`, replaces
the existing container, and waits for the health endpoint:

```bash
./rebuild-and-run.sh
```

Use a different image tag when creating a new release:

```bash
IMAGE_TAG=v2 ./rebuild-and-run.sh
```
