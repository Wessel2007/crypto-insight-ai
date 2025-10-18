# 🚀 Guia de Deployment - Crypto Insight AI

Este guia mostra diferentes formas de colocar a API em produção.

---

## 📋 Índice

1. [Deployment Local](#deployment-local)
2. [Deployment com Docker](#deployment-com-docker)
3. [Deployment em Cloud (Render, Railway, etc)](#deployment-em-cloud)
4. [Deployment em VPS](#deployment-em-vps)

---

## 1️⃣ Deployment Local

### Preparação

```bash
# Clone/navegue até o projeto
cd "Cripto Insight"

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
python run.py
```

**Ou com Gunicorn (Linux/Mac):**

```bash
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 2️⃣ Deployment com Docker

### Build e Run

```bash
# Build da imagem
docker build -t crypto-insight-ai .

# Run do container
docker run -d -p 8000:8000 --name crypto-insight crypto-insight-ai
```

### Usando Docker Compose

```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

---

## 3️⃣ Deployment em Cloud

### A. Render.com (Gratuito)

1. Faça push do código para GitHub
2. Acesse [render.com](https://render.com)
3. Crie um novo Web Service
4. Conecte seu repositório
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3

### B. Railway.app

1. Faça push do código para GitHub
2. Acesse [railway.app](https://railway.app)
3. Crie um novo projeto
4. Conecte seu repositório
5. Railway detectará automaticamente o Python e usará o Dockerfile

### C. Heroku

Crie um arquivo `Procfile`:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Deploy:

```bash
heroku create crypto-insight-ai
git push heroku main
```

### D. Google Cloud Run

```bash
# Build e push da imagem
gcloud builds submit --tag gcr.io/[PROJECT-ID]/crypto-insight-ai

# Deploy
gcloud run deploy crypto-insight-ai \
  --image gcr.io/[PROJECT-ID]/crypto-insight-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 4️⃣ Deployment em VPS (DigitalOcean, AWS EC2, etc)

### Configuração Inicial

```bash
# Conecte via SSH
ssh user@seu-servidor.com

# Atualize o sistema
sudo apt update && sudo apt upgrade -y

# Instale Python e pip
sudo apt install python3 python3-pip python3-venv -y

# Instale nginx (opcional, para proxy reverso)
sudo apt install nginx -y
```

### Setup da Aplicação

```bash
# Clone o projeto
git clone seu-repositorio.git
cd crypto-insight-ai

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Instale Gunicorn
pip install gunicorn
```

### Crie um Serviço Systemd

Crie o arquivo `/etc/systemd/system/crypto-insight.service`:

```ini
[Unit]
Description=Crypto Insight AI
After=network.target

[Service]
User=seu-usuario
WorkingDirectory=/caminho/para/crypto-insight-ai
Environment="PATH=/caminho/para/crypto-insight-ai/venv/bin"
ExecStart=/caminho/para/crypto-insight-ai/venv/bin/gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

Ative o serviço:

```bash
sudo systemctl enable crypto-insight
sudo systemctl start crypto-insight
sudo systemctl status crypto-insight
```

### Configure Nginx (Proxy Reverso)

Crie o arquivo `/etc/nginx/sites-available/crypto-insight`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Ative a configuração:

```bash
sudo ln -s /etc/nginx/sites-available/crypto-insight /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL com Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d seu-dominio.com
```

---

## 🔒 Segurança em Produção

### 1. Variáveis de Ambiente

Crie um arquivo `.env`:

```env
ENVIRONMENT=production
DEBUG=false
```

### 2. CORS

Atualize `app/main.py` para permitir apenas domínios específicos:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-frontend.com"],  # Apenas domínios permitidos
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

### 3. Rate Limiting

Instale e configure:

```bash
pip install slowapi
```

Em `app/main.py`:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/analyze/{symbol}")
@limiter.limit("10/minute")
async def analyze_symbol(request: Request, symbol: str):
    # ...
```

---

## 📊 Monitoramento

### Logs

**Docker:**
```bash
docker logs -f crypto-insight
```

**Systemd:**
```bash
journalctl -u crypto-insight -f
```

### Health Check

Configure um serviço de monitoramento (UptimeRobot, Pingdom) para verificar:
```
https://sua-api.com/health
```

---

## ⚡ Performance

### 1. Workers

Ajuste o número de workers baseado nos cores da CPU:

```bash
gunicorn app.main:app \
  --workers $(( 2 * $(nproc) + 1 )) \
  --worker-class uvicorn.workers.UvicornWorker
```

### 2. Cache

Considere adicionar Redis para cache de respostas da exchange.

### 3. CDN

Use Cloudflare ou similar para distribuir carga.

---

## 🆘 Troubleshooting

### API não responde
```bash
# Verifique se está rodando
ps aux | grep uvicorn

# Verifique logs
journalctl -u crypto-insight -n 50
```

### Erro 502 Bad Gateway
```bash
# Verifique se o serviço está ativo
sudo systemctl status crypto-insight

# Reinicie
sudo systemctl restart crypto-insight
```

### Alto uso de memória
- Reduza o número de workers
- Limite o cache de dados
- Use um servidor com mais RAM

---

**Pronto para produção! 🚀**

