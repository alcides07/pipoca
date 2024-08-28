FROM node:18

RUN npm install -g pnpm
WORKDIR /frontend
COPY package.json .
RUN pnpm install
COPY . .