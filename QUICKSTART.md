# 🚀 Guia Rápido - Crypto Insight AI

## Instalação e Execução Rápida

### 1️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 2️⃣ Rode o servidor

```bash
python run.py
```

**Ou usando Uvicorn diretamente:**
```bash
uvicorn app.main:app --reload
```

### 3️⃣ Acesse a documentação

Abra seu navegador em: http://localhost:8000/docs

---

## 📝 Testando a API

### Opção 1: Usar o navegador

Acesse: http://localhost:8000/docs

### Opção 2: Usar o script de exemplos

```bash
python examples.py
```

### Opção 3: Usar curl/PowerShell

**Health Check:**
```bash
curl http://localhost:8000/
```

**Preços do Bitcoin:**
```bash
curl http://localhost:8000/price/BTC
```

**Análise do Ethereum:**
```bash
curl http://localhost:8000/analyze/ETH
```

**Análise do Solana:**
```bash
curl http://localhost:8000/analyze/SOL
```

### Opção 4: Usar Python requests

```python
import requests

# Health Check
response = requests.get("http://localhost:8000/")
print(response.json())

# Análise do ETH
response = requests.get("http://localhost:8000/analyze/ETH")
data = response.json()
print(f"Score: {data['score']}")
print(f"Diagnóstico: {data['diagnostic']}")
```

---

## 📊 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Health check |
| GET | `/price/{symbol}` | Busca candles (1h, 4h, 1d) |
| GET | `/analyze/{symbol}` | Análise técnica completa |

**Símbolos suportados:** BTC, ETH, SOL (ou BTC/USDT, ETH/USDT, SOL/USDT)

---

## 🎯 Exemplo de Resposta do /analyze/ETH

```json
{
  "symbol": "ETH/USDT",
  "timeframes": ["1h", "4h", "1d"],
  "indicators": {
    "1h": {
      "rsi": 65.5,
      "ema9": 2150.30,
      "ema21": 2145.80,
      "ema200": 2100.50,
      "volume_ma": 15000.0,
      "macd": 12.5,
      "macd_signal": 10.2,
      "macd_histogram": 2.3
    },
    "4h": {...},
    "1d": {...}
  },
  "score": 0.72,
  "diagnostic": "Momento neutro com viés de alta leve"
}
```

---

## 🛠️ Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erro: "Address already in use"
O servidor já está rodando. Feche a instância anterior ou mude a porta:
```bash
uvicorn app.main:app --reload --port 8001
```

### Erro ao buscar dados da exchange
Verifique sua conexão com a internet. A API usa a Binance pública que não requer autenticação.

---

## ⚡ Dicas

1. **Documentação Interativa**: http://localhost:8000/docs permite testar todos os endpoints
2. **ReDoc**: http://localhost:8000/redoc para documentação alternativa
3. **Hot Reload**: O servidor recarrega automaticamente quando você modifica o código

---

## 🎓 Próximos Passos

1. Explore os diferentes símbolos (BTC, ETH, SOL)
2. Compare os indicadores entre timeframes
3. Monitore como o score muda ao longo do tempo
4. Expanda adicionando mais indicadores ou criptomoedas

---

**Pronto para começar! 🚀**

