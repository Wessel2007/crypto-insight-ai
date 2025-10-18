"""
Gerador de análises usando IA (Claude)
"""
import os
import json
from typing import Dict, Any, Optional, List
from anthropic import Anthropic


class AIAnalyzer:
    """Gerador de comentários e análises usando IA"""
    
    def __init__(self, api_key: Optional[str] = None, timeout: float = 10.0):
        """
        Inicializa o cliente da Anthropic
        
        Args:
            api_key: Chave da API Anthropic (opcional, usa variável de ambiente se não fornecida)
            timeout: Timeout para requisições à API (em segundos)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.timeout = timeout
        self.client = None
        
        if self.api_key:
            try:
                self.client = Anthropic(
                    api_key=self.api_key,
                    timeout=self.timeout
                )
            except Exception as e:
                print(f"⚠️ Aviso: Não foi possível inicializar cliente Anthropic: {e}")
    
    def generate_ai_comment(
        self, 
        indicators: Dict[str, Any], 
        score: float, 
        symbol: str = "Ativo",
        news: Optional[List[str]] = None
    ) -> str:
        """
        Gera um comentário de análise natural usando IA
        
        Args:
            indicators: Dicionário com indicadores técnicos
            score: Score de 0 a 1 (ou -1 a 1)
            symbol: Nome do ativo (ex: "Bitcoin", "Ethereum")
            news: Lista opcional de notícias recentes
            
        Returns:
            Texto de análise em 2-3 frases, natural e humano
            
        Exemplo:
            "Ethereum mostra leve força compradora nas últimas horas, 
            com RSI neutro e volume crescente. Pode haver alta leve 
            se romper resistência nos próximos candles."
        """
        # Valida parâmetros
        if not indicators or not isinstance(indicators, dict):
            return self._generate_fallback_comment({}, score, symbol)
        
        # Se não tiver cliente configurado, retorna análise básica
        if not self.client:
            return self._generate_fallback_comment(indicators, score, symbol)
        
        try:
            # Prepara dados JSON para o prompt
            data_json = {
                "symbol": symbol,
                "score": round(score, 2),
                "indicators": {
                    "RSI": indicators.get('rsi'),
                    "EMA9": indicators.get('ema9'),
                    "EMA21": indicators.get('ema21'),
                    "EMA200": indicators.get('ema200'),
                    "MACD": indicators.get('macd'),
                    "MACD_Signal": indicators.get('macd_signal'),
                    "MACD_Histogram": indicators.get('macd_histogram'),
                    "Volume_MA": indicators.get('volume_ma'),
                    "Current_Volume": indicators.get('current_volume'),
                    "ATR": indicators.get('atr'),
                    "Last_Close": indicators.get('last_close')
                },
                "news": news or []
            }
            
            # Remove valores None para limpar o JSON
            data_json["indicators"] = {k: v for k, v in data_json["indicators"].items() if v is not None}
            
            # Cria o prompt
            prompt = f"""Analise o ativo {symbol} considerando os seguintes indicadores e contexto:

{json.dumps(data_json, indent=2, ensure_ascii=False)}

INSTRUÇÕES:
- Descreva em 2-3 frases curtas e diretas
- Foque na tendência atual, riscos e oportunidades no curto prazo
- Use linguagem natural e profissional, como um analista experiente
- Não use jargões excessivos, seja claro e objetivo
- Mencione os indicadores mais relevantes de forma sutil
- Se houver notícias, considere-as no contexto

FORMATO ESPERADO:
"[Nome do ativo] mostra [tendência] nas últimas horas, com [indicador] e [indicador]. [Projeção de curto prazo]."

Responda APENAS com a análise, sem introduções ou conclusões adicionais."""

            # Chama a API Claude com timeout
            try:
                message = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=200,
                    temperature=0.7,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
            except TimeoutError:
                print(f"⚠️ Timeout ao chamar API Anthropic (>{self.timeout}s)")
                return self._generate_fallback_comment(indicators, score, symbol)
            
            # Extrai o texto da resposta
            if not message or not message.content or len(message.content) == 0:
                print(f"⚠️ Resposta vazia da API Anthropic")
                return self._generate_fallback_comment(indicators, score, symbol)
            
            comment = message.content[0].text.strip()
            
            # Remove aspas se estiverem presentes
            if comment.startswith('"') and comment.endswith('"'):
                comment = comment[1:-1]
            
            # Valida que o comentário não está vazio
            if not comment or len(comment) < 10:
                print(f"⚠️ Comentário gerado muito curto ou vazio")
                return self._generate_fallback_comment(indicators, score, symbol)
            
            return comment
            
        except TimeoutError:
            print(f"⚠️ Timeout ao gerar comentário com IA")
            return self._generate_fallback_comment(indicators, score, symbol)
        except Exception as e:
            print(f"⚠️ Erro ao gerar comentário com IA: {type(e).__name__} - {e}")
            return self._generate_fallback_comment(indicators, score, symbol)
    
    def _generate_fallback_comment(self, indicators: Dict[str, Any], score: float, symbol: str) -> str:
        """
        Gera comentário básico quando a IA não está disponível
        
        Args:
            indicators: Dicionário com indicadores técnicos
            score: Score de 0 a 1
            symbol: Nome do ativo
            
        Returns:
            Comentário básico baseado em regras
        """
        # Garante que temos um dicionário válido
        if not indicators or not isinstance(indicators, dict):
            indicators = {}
        
        # Normaliza score para 0-1 se estiver em outra escala
        if score < 0:
            score = (score + 1) / 2  # Converte de -1,1 para 0,1
        
        rsi = indicators.get('rsi')
        ema9 = indicators.get('ema9')
        ema21 = indicators.get('ema21')
        macd_histogram = indicators.get('macd_histogram')
        current_volume = indicators.get('current_volume')
        volume_ma = indicators.get('volume_ma')
        
        # Determina tendência
        if score >= 0.65:
            trend = "apresenta forte tendência de alta"
        elif score >= 0.55:
            trend = "mostra leve força compradora"
        elif score >= 0.45:
            trend = "opera em movimento lateral"
        elif score >= 0.35:
            trend = "apresenta leve pressão vendedora"
        else:
            trend = "está em tendência de baixa"
        
        # Analisa RSI
        rsi_text = ""
        if rsi:
            if rsi < 30:
                rsi_text = "RSI em zona de sobrevenda"
            elif rsi > 70:
                rsi_text = "RSI em zona de sobrecompra"
            else:
                rsi_text = "RSI neutro"
        
        # Analisa Volume
        volume_text = ""
        if current_volume and volume_ma and volume_ma > 0:
            if current_volume > volume_ma * 1.5:
                volume_text = "volume muito acima da média"
            elif current_volume > volume_ma:
                volume_text = "volume crescente"
            else:
                volume_text = "volume baixo"
        
        # Projeção
        if score >= 0.6:
            projection = "Pode haver continuação de alta se mantiver suporte."
        elif score >= 0.4:
            projection = "Recomenda-se aguardar confirmação de direção."
        else:
            projection = "Cautela recomendada no curto prazo."
        
        # Monta comentário
        parts = [f"{symbol} {trend}"]
        
        indicators_parts = []
        if rsi_text:
            indicators_parts.append(rsi_text)
        if volume_text:
            indicators_parts.append(volume_text)
        
        if indicators_parts:
            parts.append(f"com {' e '.join(indicators_parts)}")
        
        parts.append(projection)
        
        return ". ".join(parts) + "."


def generate_ai_comment(
    indicators: Dict[str, Any], 
    score: float, 
    symbol: str = "Ativo",
    news: Optional[List[str]] = None
) -> str:
    """
    Função auxiliar para gerar comentário de IA
    
    Args:
        indicators: Dicionário com indicadores técnicos
        score: Score de 0 a 1 (ou -1 a 1)
        symbol: Nome do ativo
        news: Lista opcional de notícias recentes
        
    Returns:
        Comentário natural e humano em 2-3 frases
        
    Exemplo:
        >>> indicators = {'rsi': 55, 'ema9': 42000, 'ema21': 41500}
        >>> comment = generate_ai_comment(indicators, 0.65, "Bitcoin")
        >>> print(comment)
        "Bitcoin mostra leve força compradora nas últimas horas, 
        com RSI neutro e volume crescente. Pode haver alta leve 
        se romper resistência nos próximos candles."
    """
    analyzer = AIAnalyzer()
    return analyzer.generate_ai_comment(indicators, score, symbol, news)

