# 🚀 Quick Start - AI Analyzer

Comece a usar o AI Analyzer em 3 minutos!

## ⚡ Configuração Rápida

### 1. Instalar Biblioteca

```bash
pip install anthropic
```

### 2. Configurar API Key

Obtenha sua chave em: https://console.anthropic.com/

**Linux/Mac:**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Ou crie arquivo `.env`:**
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Usar!

```python
from app.utils.ai_analyzer import generate_ai_comment

# Seus indicadores
indicators = {
    'rsi': 55.5,
    'ema9': 42000.50,
    'ema21': 41500.25,
    'current_volume': 32000000,
    'volume_ma': 25000000,
}

# Gera comentário
comment = generate_ai_comment(
    indicators=indicators,
    score=0.65,
    symbol="Bitcoin"
)

print(comment)
```

**Saída:**
```
"Bitcoin mostra leve força compradora nas últimas horas, com RSI 
neutro e volume crescente. Pode haver alta leve se romper 
resistência nos próximos candles."
```

---

## 📝 Uso Básico

### Função Principal

```python
generate_ai_comment(indicators, score, symbol, news=None)
```

**Parâmetros:**
- `indicators` (dict): Indicadores técnicos (RSI, EMAs, Volume, etc.)
- `score` (float): Score de 0.0 a 1.0
- `symbol` (str): Nome do ativo ("Bitcoin", "Ethereum", etc.)
- `news` (list, opcional): Lista de notícias recentes

**Retorna:**
- `str`: Comentário em 2-3 frases

---

## 💡 Exemplos

### Exemplo 1: Simples

```python
from app.utils.ai_analyzer import generate_ai_comment

comment = generate_ai_comment(
    indicators={'rsi': 65, 'ema9': 42000, 'ema21': 41500},
    score=0.70,
    symbol="Bitcoin"
)
```

### Exemplo 2: Com Notícias

```python
news = [
    "Bitcoin ETF approval expected",
    "Major institution adds BTC"
]

comment = generate_ai_comment(
    indicators={'rsi': 60, 'volume_ma': 25000000, 'current_volume': 35000000},
    score=0.68,
    symbol="Bitcoin",
    news=news
)
```

### Exemplo 3: Classe Direta

```python
from app.utils.ai_analyzer import AIAnalyzer

analyzer = AIAnalyzer(api_key="sua-chave-aqui")  # Opcional

comment = analyzer.generate_ai_comment(
    indicators={'rsi': 55},
    score=0.65,
    symbol="Ethereum"
)
```

---

## ⚙️ Integração na API

O comentário é gerado automaticamente no endpoint `/analyze/{symbol}`:

```python
# app/routes/analyze.py

from app.utils.ai_analyzer import generate_ai_comment

# ... dentro da rota ...

ai_comment = generate_ai_comment(
    indicators=daily_indicators,
    score=analysis['overall_score'],
    symbol=symbol_name
)

response = AnalyzeResponse(
    symbol=symbol,
    score=score,
    ai_comment=ai_comment  # Novo campo!
)
```

**Resposta JSON:**
```json
{
  "symbol": "BTC/USDT",
  "score": 0.72,
  "ai_comment": "Bitcoin apresenta forte tendência de alta...",
  "indicators": {...}
}
```

---

## 🔧 Sem API Key? Sem Problema!

O sistema tem **fallback automático**:

```python
# Mesmo sem API key, funciona!
comment = generate_ai_comment(
    indicators={'rsi': 65},
    score=0.70,
    symbol="Bitcoin"
)

# Retorna análise baseada em regras
# "Bitcoin apresenta forte tendência de alta com RSI neutro 
#  e volume crescente. Pode haver continuação de alta..."
```

---

## 🧪 Testar

Execute o arquivo de testes:

```bash
python test_ai_analyzer.py
```

Ou o arquivo de exemplos:

```bash
python example_ai_analyzer.py
```

---

## 💰 Custos

- **~$0.0075** por análise (menos de 1 centavo)
- **100 análises:** ~$0.75
- **1000 análises:** ~$7.50

Muito econômico! 🎉

---

## 📚 Mais Informações

📖 **Guia Completo:** [AI_ANALYZER_GUIDE.md](AI_ANALYZER_GUIDE.md)  
📖 **README Principal:** [README.md](README.md)  
📖 **Documentação API:** http://localhost:8000/docs

---

## ❓ Problemas Comuns

### API key não funciona

```bash
# Verifique se está configurada
echo $ANTHROPIC_API_KEY

# Reconfigure
export ANTHROPIC_API_KEY="sua-chave"
```

### Erro de importação

```bash
# Reinstale a biblioteca
pip install --upgrade anthropic
```

### Comentários muito curtos

Aumente `max_tokens` em `ai_analyzer.py`:

```python
max_tokens=300  # Era 200
```

---

**Pronto! Agora você tem análises inteligentes em linguagem natural! 🚀**

