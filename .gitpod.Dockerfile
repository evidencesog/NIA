# .gitpod.Dockerfile
FROM gitpod/workspace-full

# Install Docker inside Gitpod workspace
USER root
RUN apt-get update && apt-get install -y docker.io docker-compose && apt-get clean

USER gitpod
