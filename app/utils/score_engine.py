"""
Engine para calcular score de análise técnica
"""
from typing import Dict, Any, List


class ScoreEngine:
    """Engine para calcular scores e diagnósticos"""
    
    @staticmethod
    def _calculate_rsi_score(rsi: float) -> float:
        """
        Calcula score baseado no RSI
        
        Args:
            rsi: Valor do RSI
            
        Returns:
            Score entre -1 (oversold) e 1 (overbought)
        """
        if rsi is None:
            return 0.0
        
        if rsi <= 30:
            # Oversold - sinal de compra
            return -1.0 + (rsi / 30) * 0.5
        elif rsi >= 70:
            # Overbought - sinal de venda
            return 1.0 - ((100 - rsi) / 30) * 0.5
        else:
            # Neutro
            return (rsi - 50) / 40
    
    @staticmethod
    def _calculate_ema_score(close: float, ema9: float, ema21: float, ema200: float = None) -> float:
        """
        Calcula score baseado nas EMAs
        
        Args:
            close: Preço de fechamento atual
            ema9: EMA de 9 períodos
            ema21: EMA de 21 períodos
            ema200: EMA de 200 períodos (opcional)
            
        Returns:
            Score entre -1 (bearish) e 1 (bullish)
        """
        if ema9 is None or ema21 is None:
            return 0.0
        
        score = 0.0
        
        # Verifica se preço está acima das EMAs
        if close > ema9:
            score += 0.3
        else:
            score -= 0.3
        
        if close > ema21:
            score += 0.3
        else:
            score -= 0.3
        
        # Verifica cruzamento de EMAs
        if ema9 > ema21:
            score += 0.2  # Golden cross tendency
        else:
            score -= 0.2  # Death cross tendency
        
        # Se tiver EMA200, adiciona peso
        if ema200 is not None:
            if close > ema200:
                score += 0.2
            else:
                score -= 0.2
        
        return max(-1.0, min(1.0, score))
    
    @staticmethod
    def _calculate_macd_score(macd: float, macd_signal: float, macd_histogram: float) -> float:
        """
        Calcula score baseado no MACD
        
        Args:
            macd: Valor do MACD
            macd_signal: Linha de sinal do MACD
            macd_histogram: Histograma do MACD
            
        Returns:
            Score entre -1 (bearish) e 1 (bullish)
        """
        if macd is None or macd_signal is None or macd_histogram is None:
            return 0.0
        
        score = 0.0
        
        # MACD acima da linha de sinal é bullish
        if macd > macd_signal:
            score += 0.5
        else:
            score -= 0.5
        
        # Histograma positivo é bullish
        if macd_histogram > 0:
            score += 0.5
        else:
            score -= 0.5
        
        return score
    
    @staticmethod
    def _calculate_volume_score(current_volume: float, volume_ma: float) -> float:
        """
        Calcula score baseado no volume
        
        Args:
            current_volume: Volume atual
            volume_ma: Média móvel do volume
            
        Returns:
            Score entre 0 (baixo volume) e 1 (alto volume)
        """
        if volume_ma is None or volume_ma == 0:
            return 0.5
        
        volume_ratio = current_volume / volume_ma
        
        # Volume acima da média é positivo
        if volume_ratio > 1.5:
            return 1.0
        elif volume_ratio > 1.0:
            return 0.75
        elif volume_ratio > 0.7:
            return 0.5
        else:
            return 0.25
    
    @staticmethod
    def calculate_overall_score(indicators: Dict[str, Any], last_close: float, current_volume: float) -> float:
        """
        Calcula score geral baseado em todos os indicadores
        
        Args:
            indicators: Dicionário com todos os indicadores
            last_close: Último preço de fechamento
            current_volume: Volume atual
            
        Returns:
            Score entre 0.0 e 1.0 (0 = muito baixista, 1 = muito altista)
        """
        # Valida dados de entrada
        if not indicators or last_close is None or last_close <= 0:
            return 0.5  # Retorna neutro se dados inválidos
        
        # Calcula scores individuais
        rsi_score = ScoreEngine._calculate_rsi_score(indicators.get('rsi'))
        ema_score = ScoreEngine._calculate_ema_score(
            last_close,
            indicators.get('ema9'),
            indicators.get('ema21'),
            indicators.get('ema200')
        )
        macd_score = ScoreEngine._calculate_macd_score(
            indicators.get('macd'),
            indicators.get('macd_signal'),
            indicators.get('macd_histogram')
        )
        volume_score = ScoreEngine._calculate_volume_score(
            current_volume if current_volume else 0,
            indicators.get('volume_ma')
        )
        
        # Pesos para cada indicador
        weights = {
            'rsi': 0.25,
            'ema': 0.35,
            'macd': 0.25,
            'volume': 0.15
        }
        
        # Score ponderado (-1 a 1)
        weighted_score = (
            rsi_score * weights['rsi'] +
            ema_score * weights['ema'] +
            macd_score * weights['macd'] +
            (volume_score - 0.5) * 2 * weights['volume']  # Normaliza volume para -1 a 1
        )
        
        # Converte para 0 a 1 (garante que está no range)
        normalized_score = (weighted_score + 1) / 2
        normalized_score = max(0.0, min(1.0, normalized_score))
        
        return round(normalized_score, 2)
    
    @staticmethod
    def get_diagnostic(score: float, indicators: Dict[str, Any]) -> str:
        """
        Retorna diagnóstico baseado no score
        
        Args:
            score: Score calculado (0.0 a 1.0)
            indicators: Dicionário com indicadores
            
        Returns:
            String com diagnóstico
        """
        rsi = indicators.get('rsi', 50)
        
        if score >= 0.75:
            return "Momento fortemente altista - Tendência de alta robusta"
        elif score >= 0.65:
            return "Momento altista - Tendência de alta moderada"
        elif score >= 0.55:
            return "Momento neutro com viés de alta leve"
        elif score >= 0.45:
            return "Momento neutro - Mercado lateral"
        elif score >= 0.35:
            return "Momento neutro com viés de baixa leve"
        elif score >= 0.25:
            return "Momento baixista - Tendência de baixa moderada"
        else:
            return "Momento fortemente baixista - Tendência de baixa robusta"
    
    @staticmethod
    def analyze_multiple_timeframes(timeframes_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analisa múltiplos timeframes e retorna score consolidado
        
        Args:
            timeframes_data: Dicionário com dados de cada timeframe
            
        Returns:
            Dicionário com análise consolidada
        """
        scores = {}
        diagnostics = {}
        
        for tf, data in timeframes_data.items():
            indicators = data.get('indicators', {})
            last_close = data.get('last_close', 0)
            current_volume = data.get('current_volume', 0)
            
            score = ScoreEngine.calculate_overall_score(indicators, last_close, current_volume)
            diagnostic = ScoreEngine.get_diagnostic(score, indicators)
            
            scores[tf] = score
            diagnostics[tf] = diagnostic
        
        # Score geral (dá mais peso aos timeframes maiores)
        weights_tf = {
            '1h': 0.2,
            '4h': 0.3,
            '1d': 0.5
        }
        
        overall_score = sum(scores.get(tf, 0.5) * weight for tf, weight in weights_tf.items())
        overall_diagnostic = ScoreEngine.get_diagnostic(
            overall_score,
            timeframes_data.get('1d', {}).get('indicators', {})
        )
        
        return {
            'scores': scores,
            'diagnostics': diagnostics,
            'overall_score': round(overall_score, 2),
            'overall_diagnostic': overall_diagnostic
        }

