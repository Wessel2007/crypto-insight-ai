# 🚀 Guia de Configuração Rápida

## Passo 1: Instalar dependências

```bash
cd frontend
npm install
```

## Passo 2: Configurar variável de ambiente

Crie o arquivo `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Passo 3: Executar o projeto

```bash
npm run dev
```

Acesse: **http://localhost:3000**

## ✅ Checklist

- [ ] Backend rodando em http://localhost:8000
- [ ] Dependências instaladas (`npm install`)
- [ ] Arquivo `.env.local` criado com a URL da API
- [ ] Frontend rodando em http://localhost:3000

## 🔧 Resolução de Problemas

### Erro de conexão com API

- Verifique se o backend está rodando
- Confirme a URL no `.env.local`
- Verifique o CORS no backend

### Erro ao instalar dependências

```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Porta 3000 já está em uso

```bash
# Rodar em outra porta
npm run dev -- -p 3001
```

