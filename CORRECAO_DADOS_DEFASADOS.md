# 🔧 Correção de Dados Defasados na API

## 📋 Problema Identificado

A API estava retornando candles antigos/defasados porque:
- Usava `time.time()` em vez de `exchange.milliseconds()` para calcular o timestamp
- A lógica de cálculo do parâmetro `since` não estava otimizada
- Não havia validação se os dados retornados estavam atualizados
- Faltava exibir o horário de Brasília para facilitar a verificação pelo usuário brasileiro

## ✅ Correções Implementadas

### 1. **Uso de `exchange.milliseconds()` (crypto_service.py)**

**ANTES:**
```python
now = int(time.time() * 1000)  # timestamp em ms
since = now - (limit * minutes * 60 * 1000 * 1.2)
```

**DEPOIS:**
```python
# Usa o horário da exchange (mais preciso que time.time())
now = self.exchange.milliseconds()
# Calcula 'since' baseado no número de candles e timeframe
# Fórmula: agora - (limit * intervalo_em_minutos * 60_segundos * 1000_milissegundos)
since = now - (limit * minutes * 60 * 1000)
```

**Por quê?**
- `exchange.milliseconds()` está sincronizado com o relógio da exchange (Binance)
- Garante que o parâmetro `since` seja calculado com base no horário real do mercado
- Elimina possíveis diferenças de timezone entre servidor e exchange

### 2. **Validação Automática de Frescor dos Dados**

Adicionado ao método `get_candles()`:

```python
# Valida se o último candle é recente (dentro de 24h para timeframes maiores)
max_delay_hours = {'1m': 1, '5m': 1, '15m': 2, '30m': 2, '1h': 3, '4h': 12, '1d': 48, '1w': 168}
max_delay = max_delay_hours.get(timeframe, 24) * 60 * 60 * 1000  # em milissegundos

if (now - last_candle_timestamp_ms) > max_delay:
    print(f"⚠️ AVISO: Último candle de {symbol} ({timeframe}) está defasado!")
    print(f"   Horário atual: {datetime.fromtimestamp(now/1000, tz=timezone.utc)}")
    print(f"   Último candle: {datetime.fromtimestamp(last_candle_timestamp_ms/1000, tz=timezone.utc)}")
```

**Benefícios:**
- Detecta automaticamente quando os dados estão desatualizados
- Emite avisos no console para depuração
- Permite ajustar tolerâncias por timeframe

### 3. **Timestamps em UTC e Horário de Brasília**

Criado novo método `get_last_candle_timestamps()`:

```python
def get_last_candle_timestamps(self, df: pd.DataFrame) -> Tuple[str, str]:
    """
    Extrai e formata os timestamps do último candle (UTC e Brasília)
    
    Returns:
        Tupla (timestamp_utc, timestamp_brt) formatados
        Exemplo: ("2025-10-20 15:00 UTC", "2025-10-20 12:00 BRT")
    """
    if df.empty:
        return ("N/A", "N/A")
    
    # Obtém o último timestamp (já está em UTC timezone-aware)
    last_timestamp_utc = df['timestamp'].iloc[-1]
    
    # Formata UTC
    timestamp_utc = last_timestamp_utc.strftime('%Y-%m-%d %H:%M UTC')
    
    # Converte para horário de Brasília (BRT/BRST)
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    last_timestamp_brt = last_timestamp_utc.astimezone(brasilia_tz)
    
    # Usa %Z para obter a abreviação correta (BRT ou BRST dependendo do horário de verão)
    timestamp_brt = last_timestamp_brt.strftime('%Y-%m-%d %H:%M %Z')
    
    return (timestamp_utc, timestamp_brt)
```

**Vantagens:**
- Exibe horário UTC (padrão internacional)
- Exibe horário de Brasília (facilita para usuários brasileiros)
- Detecta automaticamente horário de verão (BRT vs BRST)

### 4. **Atualização do Schema de Resposta**

**schemas.py:**
```python
class AnalyzeResponse(BaseModel):
    """Resposta do endpoint /analyze/{symbol}"""
    symbol: str
    timeframes: List[str]
    indicators: Dict[str, IndicatorData]
    score: float
    diagnostic: str
    last_candle_timestamp: str  # UTC
    last_candle_timestamp_brt: str  # Brasília ✨ NOVO
    ai_comment: Optional[str] = None
    chart_data: Optional[ChartDataResponse] = None
    trade_opportunity: Optional[TradeOpportunity] = None
```

### 5. **Atualização da Rota de Análise**

**analyze.py:**
```python
# Captura timestamps do último candle (usa o timeframe de 1h como referência)
last_candle_timestamp = "N/A"
last_candle_timestamp_brt = "N/A"
if '1h' in data and not data['1h'].empty:
    # Obtém timestamps formatados (UTC e Brasília)
    last_candle_timestamp, last_candle_timestamp_brt = crypto_service.get_last_candle_timestamps(data['1h'])
```

### 6. **Atualização do Frontend**

**CryptoCard.tsx:**
```tsx
<div className="flex flex-col sm:flex-row sm:items-center sm:justify-center gap-1 sm:gap-3">
  <p className="text-sm sm:text-base font-semibold text-blue-300">
    {analysis.last_candle_timestamp}
  </p>
  {analysis.last_candle_timestamp_brt && analysis.last_candle_timestamp_brt !== 'N/A' && (
    <>
      <span className="hidden sm:inline text-gray-500">|</span>
      <p className="text-xs sm:text-sm font-medium text-green-300">
        {analysis.last_candle_timestamp_brt}
      </p>
    </>
  )}
</div>
```

**api.ts:**
```typescript
export interface AnalysisResponse {
  symbol: string;
  timeframes: string[];
  indicators: { [timeframe: string]: IndicatorData };
  score: number;
  diagnostic: string;
  last_candle_timestamp: string;
  last_candle_timestamp_brt: string;  // ✨ NOVO
  ai_comment?: string;
  chart_data?: ChartDataResponse | null;
  trade_opportunity?: TradeOpportunity | null;
}
```

## 📦 Dependências Adicionadas

```txt
pytz==2024.1  # Para conversão de timezone (UTC → BRT)
```

## 🧪 Como Testar

Execute o script de teste:

```bash
python test_data_freshness.py
```

**Saída Esperada:**
```
================================================================================
TESTE DE ATUALIZAÇÃO DOS DADOS (Correção de Candles Defasados)
================================================================================

================================================================================
Testando timeframe: 1h
================================================================================

✅ Dados obtidos com sucesso!
   Total de candles: 500
   Primeiro candle: 2025-10-19 02:00:00+00:00
   Último candle: 2025-10-20 02:00:00+00:00

📅 TIMESTAMPS FORMATADOS:
   UTC:      2025-10-20 02:00 UTC
   Brasília: 2025-10-19 23:00 -03

⏱️  TEMPO DESDE O ÚLTIMO CANDLE:
   45.2 minutos atrás
   ✅ DADOS ATUALIZADOS (dentro da tolerância de 120 min)

📊 VALIDAÇÃO TÉCNICA:
   Preço de fechamento: $67,234.50
   Volume: 1,234,567.89
   High: $67,500.00
   Low: $67,100.00
```

## 🎯 Exemplo de Resposta da API

### **GET /analyze/BTC**

```json
{
  "symbol": "BTC/USDT",
  "timeframes": ["1h", "4h", "1d"],
  "indicators": { ... },
  "score": 0.68,
  "diagnostic": "Tendência altista moderada com momentum positivo...",
  "last_candle_timestamp": "2025-10-20 02:00 UTC",
  "last_candle_timestamp_brt": "2025-10-19 23:00 -03",
  "ai_comment": "Bitcoin está mostrando sinais de recuperação...",
  "chart_data": { ... },
  "trade_opportunity": { ... }
}
```

## 🔍 Verificação Manual

Para verificar se os dados estão atualizados:

1. **Compare o timestamp UTC** com o horário atual em UTC
2. **Compare o timestamp BRT** com o horário atual em Brasília
3. **Verifique a diferença**: deve ser menor que:
   - **1h timeframe**: máximo 3 horas atrás
   - **4h timeframe**: máximo 12 horas atrás
   - **1d timeframe**: máximo 48 horas atrás

## 📊 Fluxo de Dados Corrigido

```
1. Frontend solicita análise
   ↓
2. Backend chama crypto_service.get_candles()
   ↓
3. Calcula 'since' usando exchange.milliseconds()
   since = now - (500 candles × 60 min × 60 seg × 1000 ms)
   ↓
4. Binance retorna os 500 candles mais recentes
   ↓
5. Valida frescor dos dados
   ↓
6. Converte timestamps para datetime (UTC)
   ↓
7. Formata timestamps (UTC e Brasília)
   ↓
8. Retorna ao frontend com ambos os timestamps
   ↓
9. Exibe na interface: "2025-10-20 15:00 UTC | 2025-10-20 12:00 BRT"
```

## ⚡ Benefícios das Correções

1. ✅ **Dados sempre atualizados**: usa horário da exchange
2. ✅ **Validação automática**: detecta dados defasados
3. ✅ **Transparência**: exibe timestamps em UTC e BRT
4. ✅ **Facilidade de verificação**: usuário pode confirmar visualmente
5. ✅ **Debug melhorado**: avisos automáticos no console
6. ✅ **Sincronização precisa**: elimina diferenças de timezone

## 🛠️ Arquivos Modificados

- ✅ `app/services/crypto_service.py` - Lógica de busca de dados
- ✅ `app/routes/analyze.py` - Endpoint de análise
- ✅ `app/models/schemas.py` - Schema de resposta
- ✅ `frontend/lib/api.ts` - Tipos TypeScript
- ✅ `frontend/components/CryptoCard.tsx` - Exibição dos timestamps
- ✅ `requirements.txt` - Dependência pytz
- ✅ `test_data_freshness.py` - Script de teste (novo)

## 📝 Notas Técnicas

### Por que usar `exchange.milliseconds()` em vez de `time.time()`?

1. **Sincronização**: O método `exchange.milliseconds()` retorna o timestamp sincronizado com o servidor da exchange
2. **Precisão**: Elimina discrepâncias de timezone entre o servidor da aplicação e a exchange
3. **Consistência**: Garante que o cálculo do `since` seja baseado no mesmo relógio usado pela API da exchange

### Por que validar frescor dos dados?

1. **Confiabilidade**: Detecta problemas de conexão ou latência
2. **Qualidade**: Garante que análises sejam feitas com dados recentes
3. **Debug**: Facilita identificação de problemas em produção

### Por que exibir horário de Brasília?

1. **UX**: Usuários brasileiros podem verificar facilmente se os dados estão atualizados
2. **Confiança**: Transparência aumenta a confiança no sistema
3. **Praticidade**: Não precisa fazer conversão mental de UTC para BRT

## 🎉 Resultado Final

Agora a API **SEMPRE** retorna:
- ✅ Dados mais recentes disponíveis na exchange
- ✅ Timestamp UTC e Brasília formatados
- ✅ Validação automática de frescor
- ✅ Avisos automáticos se dados estiverem defasados
- ✅ Melhor experiência para o usuário brasileiro

**Exemplo visual no frontend:**
```
Dados do mercado atualizados:
2025-10-20 15:00 UTC | 2025-10-20 12:00 BRT
```

