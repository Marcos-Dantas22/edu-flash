# Use uma imagem oficial Node.js para build e runtime
FROM node:18-alpine AS builder

WORKDIR /app

# Copia package.json e package-lock para instalar dependências
COPY package*.json ./

# Instala dependências (prod + dev para build)
RUN npm install

# Copia todo o código fonte
COPY . .

# Expõe a porta padrão Next.js
EXPOSE 3000

# Build da aplicação Next.js
RUN npm run build

# Comando para iniciar a aplicação em modo produção
# CMD ["npm", "start"]
