# 🚀 Crypto Insight AI - Frontend

Interface moderna e intuitiva para análise de criptomoedas com inteligência artificial.

## 🛠️ Tecnologias

- **Next.js 14** - Framework React com SSR
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização moderna e responsiva
- **Axios** - Cliente HTTP para API
- **Lucide React** - Ícones modernos

## 📦 Instalação

### 1. Instalar dependências

```bash
npm install
# ou
yarn install
# ou
pnpm install
```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env.local` na raiz do projeto:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

> **Nota:** Certifique-se de que o backend está rodando na porta especificada.

### 3. Executar em modo de desenvolvimento

```bash
npm run dev
# ou
yarn dev
# ou
pnpm dev
```

Acesse [http://localhost:3000](http://localhost:3000) no navegador.

## 🏗️ Estrutura do Projeto

```
frontend/
├── components/
│   └── CryptoCard.tsx       # Componente de card de criptomoeda
├── lib/
│   └── api.ts               # Cliente API e tipos TypeScript
├── pages/
│   ├── _app.tsx             # Configuração global do app
│   ├── _document.tsx        # Documento HTML customizado
│   └── index.tsx            # Página principal
├── styles/
│   └── globals.css          # Estilos globais + Tailwind
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

## 🎨 Funcionalidades

- ✅ **Análise em tempo real** de BTC, ETH e SOL
- ✅ **Score de confiança** visual com barra de progresso
- ✅ **Indicadores técnicos** (RSI, EMA, Volume, etc.)
- ✅ **Diagnóstico e recomendações** gerados por IA
- ✅ **Dark mode** nativo e design moderno
- ✅ **Totalmente responsivo** para mobile e desktop
- ✅ **Animações suaves** e feedback visual

## 🔗 Integração com Backend

O frontend se comunica com o backend através da API REST:

- `GET /analyze/{symbol}` - Análise completa da criptomoeda
- `GET /price/{symbol}` - Preço atual e dados de mercado

Todas as requisições são feitas através do módulo `lib/api.ts`.

## 🚀 Build para Produção

```bash
npm run build
npm run start
```

## 📝 Comandos Disponíveis

- `npm run dev` - Inicia servidor de desenvolvimento
- `npm run build` - Cria build de produção
- `npm run start` - Inicia servidor de produção
- `npm run lint` - Executa o linter

## 🎯 Próximos Passos

- [ ] Adicionar gráficos de preço histórico
- [ ] Implementar sistema de alertas
- [ ] Adicionar mais criptomoedas
- [ ] Dashboard com múltiplas moedas
- [ ] Modo claro/escuro toggle
- [ ] Notificações em tempo real

## ⚠️ Aviso Legal

As análises fornecidas são apenas para fins informativos e educacionais. Não constituem aconselhamento financeiro ou recomendação de investimento.

---

Desenvolvido com ❤️ usando Next.js + TypeScript + Tailwind CSS

