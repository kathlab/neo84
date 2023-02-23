# neo84
neo84 is a Matrix42 compatible package creator. 

Build docker image:
---

```
$ docker build -f Dockerfile -t local/neo84:latest .
```

Create and run docker container:
---

```
$ docker compose up -d
```

Run VS Code inside docker container
---

1. Open VS Code workspace
2. (optional) Add ports forwarding of 8888 and 8889 in VS Code (for Juypter Notebook web app)
3. Dev Containers: Reopen in Container
4. Install VS Code extensions as needed