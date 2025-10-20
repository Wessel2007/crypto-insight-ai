# 🚀 Guia Prático de Validação - Auditoria Backend

## ⚡ Início Rápido (2 minutos)

### Passo 1: Inicie a API
```bash
python run.py
```

Aguarde até ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Passo 2: Execute o Teste Automatizado
Em outro terminal:
```bash
python test_auditoria_realtime.py
```

### Passo 3: Veja os Resultados
O teste irá:
- ✅ Fazer requisições para BTC, ETH e SOL
- ✅ Validar que o campo `last_candle_timestamp` existe
- ✅ Verificar que os dados estão sendo atualizados
- ✅ Mostrar exemplos do JSON retornado

---

## 🧪 Testes Manuais

### Teste 1: Verificar Timestamp
```bash
curl http://localhost:8000/analyze/BTC | jq '.last_candle_timestamp'
```

**Resultado Esperado:**
```
"2025-10-20 15:00 UTC"
```

### Teste 2: Ver Indicadores Completos
```bash
curl http://localhost:8000/analyze/BTC | jq '.indicators."1h"'
```

**Resultado Esperado:**
```json
{
  "trend": {
    "EMA9": 67891.23,
    "EMA21": 67654.32,
    "EMA50": 66987.45,
    "EMA200": 64321.10,
    "SMA100": 65876.54
  },
  "momentum": {
    "RSI": 64.25,
    "Stochastic_RSI_K": 72.15,
    "Stochastic_RSI_D": 68.92,
    "MACD": 234.56,
    "MACD_Signal": 198.34,
    "MACD_Histogram": 36.22
  },
  "volatility": {
    "ATR": 1456.78,
    "BB_Upper": 69200.00,
    "BB_Middle": 67800.00,
    "BB_Lower": 66400.00
  },
  "volume": {
    "Volume_MA": 18234.56,
    "MFI": 62.45,
    "OBV": 987654321
  },
  "strength": {
    "ADX": 28.56
  },
  "price": {
    "last_close": 67891.23,
    "current_volume": 21543.21
  }
}
```

### Teste 3: Verificar Score
```bash
curl http://localhost:8000/analyze/BTC | jq '{score: .score, diagnostic: .diagnostic, timestamp: .last_candle_timestamp}'
```

**Resultado Esperado:**
```json
{
  "score": 0.72,
  "diagnostic": "Alta probabilidade de alta",
  "timestamp": "2025-10-20 15:00 UTC"
}
```

---

## 🔍 Como Validar Dados em Tempo Real

### Teste Duplo (comprova atualização)
```bash
# Requisição 1
echo "=== PRIMEIRA REQUISIÇÃO ==="
curl http://localhost:8000/analyze/BTC | jq '{timestamp: .last_candle_timestamp, price: .indicators."1h".price.last_close, rsi: .indicators."1h".momentum.RSI}'

# Aguarda 30 segundos
sleep 30

# Requisição 2
echo "=== SEGUNDA REQUISIÇÃO ==="
curl http://localhost:8000/analyze/BTC | jq '{timestamp: .last_candle_timestamp, price: .indicators."1h".price.last_close, rsi: .indicators."1h".momentum.RSI}'
```

**O que observar:**
- Se o timestamp mudou = novo candle disponível
- Se o preço mudou = dados sendo atualizados
- Se RSI mudou = indicadores recalculados

---

## 📊 Validação por Criptomoeda

### Bitcoin
```bash
curl http://localhost:8000/analyze/BTC
```

### Ethereum
```bash
curl http://localhost:8000/analyze/ETH
```

### Solana
```bash
curl http://localhost:8000/analyze/SOL
```

---

## ✅ Checklist de Validação

Use este checklist para confirmar que tudo está funcionando:

### Estrutura da Resposta
- [ ] Campo `symbol` presente
- [ ] Campo `timeframes` com ["1h", "4h", "1d"]
- [ ] Campo `score` entre 0 e 1
- [ ] Campo `diagnostic` com texto
- [ ] Campo `last_candle_timestamp` presente ⭐ **NOVO**
- [ ] Campo `indicators` com dados dos 3 timeframes
- [ ] Campo `ai_comment` (opcional)
- [ ] Campo `trade_opportunity` (opcional)

### Indicadores por Timeframe
Para cada timeframe (1h, 4h, 1d):
- [ ] `trend`: EMA9, EMA21, EMA50, EMA200, SMA100
- [ ] `momentum`: RSI, Stochastic_RSI_K, Stochastic_RSI_D, MACD, MACD_Signal, MACD_Histogram
- [ ] `volatility`: ATR, BB_Upper, BB_Middle, BB_Lower
- [ ] `volume`: Volume_MA, MFI, OBV
- [ ] `strength`: ADX
- [ ] `price`: last_close, current_volume

### Timestamp
- [ ] Formato: "YYYY-MM-DD HH:MM UTC"
- [ ] Exemplo: "2025-10-20 15:00 UTC"
- [ ] Horário recente (máximo 1 hora atrás para timeframe 1h)

---

## 🐛 Troubleshooting

### Problema: API não inicia
**Solução:**
```bash
# Instale dependências
pip install -r requirements.txt

# Tente novamente
python run.py
```

### Problema: Erro "Connection refused"
**Solução:**
```bash
# Verifique se a API está rodando
curl http://localhost:8000/

# Deve retornar: {"status":"ok"}
```

### Problema: Campo `last_candle_timestamp` não aparece
**Solução:**
```bash
# Certifique-se de ter puxado as mudanças mais recentes
git pull

# Reinicie a API
# Ctrl+C para parar
python run.py
```

### Problema: Timestamp sempre "N/A"
**Solução:**
- Verifique conexão com a internet
- Tente outro símbolo: `curl http://localhost:8000/analyze/ETH`
- Veja logs da API para erros

---

## 📝 Exemplo de Teste Completo

```bash
#!/bin/bash

echo "🚀 Iniciando validação completa..."
echo ""

# Teste 1: Health check
echo "1️⃣ Testando health check..."
curl -s http://localhost:8000/ | jq
echo ""

# Teste 2: Análise BTC
echo "2️⃣ Analisando Bitcoin..."
RESPONSE=$(curl -s http://localhost:8000/analyze/BTC)
echo "$RESPONSE" | jq '{
  symbol: .symbol,
  timestamp: .last_candle_timestamp,
  score: .score,
  diagnostic: .diagnostic,
  price: .indicators."1h".price.last_close,
  rsi: .indicators."1h".momentum.RSI
}'
echo ""

# Teste 3: Valida timestamp
echo "3️⃣ Validando timestamp..."
TIMESTAMP=$(echo "$RESPONSE" | jq -r '.last_candle_timestamp')
if [ "$TIMESTAMP" != "N/A" ] && [ "$TIMESTAMP" != "null" ]; then
    echo "✅ Timestamp válido: $TIMESTAMP"
else
    echo "❌ Timestamp inválido: $TIMESTAMP"
fi
echo ""

# Teste 4: Valida indicadores
echo "4️⃣ Validando indicadores..."
RSI=$(echo "$RESPONSE" | jq -r '.indicators."1h".momentum.RSI')
EMA9=$(echo "$RESPONSE" | jq -r '.indicators."1h".trend.EMA9')
ADX=$(echo "$RESPONSE" | jq -r '.indicators."1h".strength.ADX')

if [ "$RSI" != "null" ]; then
    echo "✅ RSI: $RSI"
else
    echo "❌ RSI não encontrado"
fi

if [ "$EMA9" != "null" ]; then
    echo "✅ EMA9: $EMA9"
else
    echo "❌ EMA9 não encontrada"
fi

if [ "$ADX" != "null" ]; then
    echo "✅ ADX: $ADX"
else
    echo "❌ ADX não encontrado"
fi

echo ""
echo "🎉 Validação concluída!"
```

Salve como `validacao_completa.sh` e execute:
```bash
chmod +x validacao_completa.sh
./validacao_completa.sh
```

---

## 📈 Interpretando os Resultados

### Score
- **0.7 - 1.0**: Alta probabilidade de alta (bullish forte)
- **0.4 - 0.69**: Tendência neutra com leve viés de alta
- **0.0 - 0.39**: Baixa probabilidade de alta / possível queda (bearish)

### RSI
- **> 70**: Sobrecompra (overbought) - possível correção
- **50 - 70**: Momentum positivo
- **30 - 50**: Momentum neutro/negativo
- **< 30**: Sobrevenda (oversold) - possível recuperação

### ADX
- **> 25**: Tendência forte
- **20 - 25**: Tendência moderada
- **< 20**: Tendência fraca / lateralização

### MACD Histogram
- **> 0**: Momentum de alta
- **< 0**: Momentum de baixa

---

## 🎯 Validação Rápida (30 segundos)

```bash
# Teste tudo de uma vez
curl -s http://localhost:8000/analyze/BTC | jq '{
  "✅ Símbolo": .symbol,
  "✅ Timestamp": .last_candle_timestamp,
  "✅ Score": .score,
  "✅ Diagnóstico": .diagnostic,
  "✅ Preço": .indicators."1h".price.last_close,
  "✅ RSI": .indicators."1h".momentum.RSI,
  "✅ MACD": .indicators."1h".momentum.MACD,
  "✅ ADX": .indicators."1h".strength.ADX
}'
```

**Saída esperada:**
```json
{
  "✅ Símbolo": "BTC/USDT",
  "✅ Timestamp": "2025-10-20 15:00 UTC",
  "✅ Score": 0.72,
  "✅ Diagnóstico": "Alta probabilidade de alta",
  "✅ Preço": 67891.23,
  "✅ RSI": 64.25,
  "✅ MACD": 234.56,
  "✅ ADX": 28.56
}
```

---

## 🏁 Conclusão

Se todos os testes passaram, você confirmou que:

✅ Dados são buscados em tempo real  
✅ Indicadores são recalculados a cada requisição  
✅ Timestamp do último candle é retornado  
✅ Nenhum valor é armazenado entre análises  
✅ Sistema está pronto para uso

---

**Dúvidas?** Consulte:
- `AUDITORIA_BACKEND_REALTIME.md` - Documentação técnica
- `RESUMO_AUDITORIA.md` - Resumo visual
- `EXEMPLO_COMPARACAO_API.md` - Exemplos práticos

