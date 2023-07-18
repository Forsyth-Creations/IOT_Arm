# Stage 1: Spawn the builder image

FROM ubuntu:kinetic

ENV NODE_VERSION 19.3.0
ENV NPM_VERSION 9.8.0


# replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# --------------- Build the Application ---------------

# Copy over all needed files

WORKDIR /app

# Update the container and install dependencies

ARG apt_deps
RUN apt-get update && \
    apt-get install -y $apt_deps

# install curl

RUN apt-get update \
    && apt-get install -y curl \
    && apt-get -y autoclean

# -------------------------------- install nvm ------------------------------------------

ENV NVM_DIR /usr/local/nvm

RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash

# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
RUN npm install -g npm@$NPM_VERSION

# -----------------------------------------------------------------------------------------

COPY . .

# build react app with npm
RUN npm install --legacy-peer-deps

# Get the environment set up
# ENV HTTPS true

EXPOSE 3000

WORKDIR /app

# # Stage 2: Copy the .next folder from the builder image, and run it here with node

# FROM node:19.3.0-alpine

# WORKDIR /app

# COPY --from=0 /app/.next .next
# COPY --from=0 /app/package.json ./package.json
# COPY --from=0 /app/public ./public

# # Install dependencies
# RUN npm install --omit=dev