# 🤖 Guia do AI Analyzer

Sistema de geração de comentários naturais usando IA (Claude/Anthropic) para análise de criptomoedas.

## 📋 Visão Geral

O **AI Analyzer** gera análises em linguagem natural e profissional baseadas em indicadores técnicos, substituindo diagnósticos mecânicos por textos humanizados e contextualizados.

### Exemplo de Saída

**Antes (diagnóstico mecânico):**
```
"Momento fortemente altista - Tendência de alta robusta"
```

**Depois (comentário com IA):**
```
"Ethereum mostra leve força compradora nas últimas horas, com RSI neutro 
e volume crescente. Pode haver alta leve se romper resistência nos 
próximos candles."
```

---

## 🚀 Instalação e Configuração

### 1. Instalar Dependências

```bash
pip install anthropic==0.25.0
```

Ou com o requirements.txt atualizado:

```bash
pip install -r requirements.txt
```

### 2. Obter API Key da Anthropic

1. Acesse [console.anthropic.com](https://console.anthropic.com/)
2. Crie uma conta ou faça login
3. Vá em **API Keys** e gere uma nova chave
4. Copie a chave (começa com `sk-ant-api03-...`)

### 3. Configurar Variável de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Ou exporte diretamente (Linux/Mac):

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Windows PowerShell:

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## 💻 Como Usar

### Uso Básico

```python
from app.utils.ai_analyzer import generate_ai_comment

# Seus indicadores técnicos
indicators = {
    'rsi': 55.5,
    'ema9': 42000.50,
    'ema21': 41500.25,
    'ema200': 40000.00,
    'macd': 150.25,
    'macd_histogram': 4.75,
    'volume_ma': 25000000,
    'current_volume': 32000000,
}

# Gera comentário
comment = generate_ai_comment(
    indicators=indicators,
    score=0.65,
    symbol="Bitcoin",
    news=None  # Opcional
)

print(comment)
# "Bitcoin apresenta forte tendência de alta com RSI neutro e 
#  volume 28% acima da média. Rompimento de resistência em 42.5k 
#  pode impulsionar movimento de alta no curto prazo."
```

### Com Notícias

```python
news = [
    "Bitcoin ETF approval expected this week",
    "Major institution adds BTC to balance sheet"
]

comment = generate_ai_comment(
    indicators=indicators,
    score=0.70,
    symbol="Bitcoin",
    news=news
)
```

### Integração na API

O comentário é gerado automaticamente no endpoint `/analyze/{symbol}`:

```python
# app/routes/analyze.py
from app.utils.ai_analyzer import generate_ai_comment

# ... código da rota ...

ai_comment = generate_ai_comment(
    indicators=daily_indicators,
    score=analysis['overall_score'],
    symbol=symbol_name,
    news=None
)

response = AnalyzeResponse(
    symbol=normalized_symbol,
    score=analysis['overall_score'],
    diagnostic=analysis['overall_diagnostic'],
    ai_comment=ai_comment  # ✨ Novo campo
)
```

---

## 🎯 Funcionalidades

### ✅ Geração com IA (Claude)

- Análise contextualizada e natural
- Considera todos os indicadores técnicos
- Linguagem profissional e objetiva
- 2-3 frases diretas e informativas
- Modelo: `claude-3-5-sonnet-20241022`

### ✅ Fallback Inteligente

Se a API key não estiver configurada ou houver erro:

- Sistema gera análise baseada em regras
- Mantém qualidade e contexto
- Não interrompe o fluxo da aplicação

```python
# Exemplo de fallback
"Bitcoin apresenta forte tendência de alta com RSI neutro e volume 
crescente. Pode haver continuação de alta se mantiver suporte."
```

### ✅ Suporte a Notícias

```python
news = ["Bitcoin ETF approved", "Institutional buying increases"]

# IA considera notícias no contexto
comment = generate_ai_comment(indicators, 0.75, "Bitcoin", news)
```

---

## 📊 Estrutura da Resposta

### Resposta da API

```json
{
  "symbol": "BTC/USDT",
  "score": 0.65,
  "diagnostic": "Momento altista - Tendência de alta moderada",
  "ai_comment": "Bitcoin mostra leve força compradora nas últimas horas, com RSI neutro e volume crescente. Pode haver alta leve se romper resistência nos próximos candles.",
  "indicators": { ... },
  "timeframes": ["1h", "4h", "1d"]
}
```

---

## 🔧 Personalização

### Modelo de IA

Você pode alterar o modelo no código:

```python
# app/utils/ai_analyzer.py
message = self.client.messages.create(
    model="claude-3-5-sonnet-20241022",  # Modelo atual
    max_tokens=200,
    temperature=0.7,
    messages=[{"role": "user", "content": prompt}]
)
```

### Prompt Template

O prompt pode ser customizado em `ai_analyzer.py`:

```python
prompt = f"""Analise o ativo {symbol} considerando os seguintes indicadores:
{json.dumps(data_json, indent=2)}

INSTRUÇÕES:
- Descreva em 2-3 frases
- Foque na tendência, riscos e oportunidades
- Use linguagem profissional
"""
```

---

## 🧪 Testes

Execute os testes do AI Analyzer:

```bash
python test_ai_analyzer.py
```

**Testes disponíveis:**
- ✅ Geração com tendência positiva
- ✅ Geração com tendência negativa
- ✅ Mercado neutro
- ✅ Análise com notícias
- ✅ Fallback sem API key

---

## 💰 Custos

### Anthropic API Pricing (Claude 3.5 Sonnet)

- **Input:** $3.00 / 1M tokens
- **Output:** $15.00 / 1M tokens

### Estimativa por Análise

- Cada análise usa ~500 tokens (input + output)
- **Custo por análise:** ~$0.0075 (menos de 1 centavo)
- **100 análises:** ~$0.75
- **1000 análises:** ~$7.50

**Muito econômico para uso em produção! 🎉**

---

## 🛡️ Segurança

### Boas Práticas

1. **Nunca commite a API key** no Git
2. Use variáveis de ambiente (`.env`)
3. Adicione `.env` ao `.gitignore`
4. Configure limites de rate limiting
5. Monitore uso no console da Anthropic

### Exemplo .gitignore

```
.env
.env.local
*.key
secrets/
```

---

## 🔍 Troubleshooting

### Erro: "API key not found"

```bash
# Verifique se a variável está configurada
echo $ANTHROPIC_API_KEY

# Configure se necessário
export ANTHROPIC_API_KEY="sua-chave-aqui"
```

### Fallback sendo usado sempre

- Verifique se a API key está correta
- Teste conexão com API da Anthropic
- Verifique logs de erro no console

### Comentários muito genéricos

- Aumente `max_tokens` de 200 para 300
- Ajuste `temperature` para 0.8-0.9
- Melhore o prompt com mais contexto

---

## 📚 Referências

- [Documentação Anthropic](https://docs.anthropic.com/)
- [Claude API Reference](https://docs.anthropic.com/claude/reference)
- [Best Practices](https://docs.anthropic.com/claude/docs/best-practices)

---

## 🎯 Próximos Passos

- [ ] Integração com `news_fetcher.py` para notícias reais
- [ ] Cache de comentários para reduzir custos
- [ ] Análise comparativa (BTC vs ETH)
- [ ] Geração de relatórios em português
- [ ] Suporte a múltiplos idiomas

---

**Desenvolvido com ❤️ usando Claude AI**

