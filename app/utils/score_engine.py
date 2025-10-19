"""
Engine para calcular score de análise técnica
"""
from typing import Dict, Any, List


class ScoreEngine:
    """Engine para calcular scores e diagnósticos"""
    
    @staticmethod
    def _flatten_indicators(indicators: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converte a nova estrutura de indicadores (categorizada) para o formato flat
        usado pelos métodos de cálculo de score (compatibilidade retroativa)
        
        Args:
            indicators: Indicadores no novo formato (com categorias) ou formato antigo (flat)
            
        Returns:
            Indicadores no formato flat
        """
        # Se já está no formato flat (chave 'rsi' existe diretamente), retorna como está
        if 'rsi' in indicators:
            return indicators
        
        # Se está no formato novo (com categorias), converte para flat
        flat = {}
        
        # Trend
        trend = indicators.get('trend', {})
        flat['ema9'] = trend.get('EMA9')
        flat['ema21'] = trend.get('EMA21')
        flat['ema50'] = trend.get('EMA50')
        flat['ema200'] = trend.get('EMA200')
        flat['sma100'] = trend.get('SMA100')
        
        # Momentum
        momentum = indicators.get('momentum', {})
        flat['rsi'] = momentum.get('RSI')
        flat['stoch_rsi_k'] = momentum.get('Stochastic_RSI_K')
        flat['stoch_rsi_d'] = momentum.get('Stochastic_RSI_D')
        flat['macd'] = momentum.get('MACD')
        flat['macd_signal'] = momentum.get('MACD_Signal')
        flat['macd_histogram'] = momentum.get('MACD_Histogram')
        
        # Volatility
        volatility = indicators.get('volatility', {})
        flat['atr'] = volatility.get('ATR')
        flat['bb_upper'] = volatility.get('BB_Upper')
        flat['bb_middle'] = volatility.get('BB_Middle')
        flat['bb_lower'] = volatility.get('BB_Lower')
        
        # Volume
        volume = indicators.get('volume', {})
        flat['volume_ma'] = volume.get('Volume_MA')
        flat['mfi'] = volume.get('MFI')
        flat['obv'] = volume.get('OBV')
        
        # Strength
        strength = indicators.get('strength', {})
        flat['adx'] = strength.get('ADX')
        
        return flat
    
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
    def _calculate_stochastic_score(stoch_k: float, stoch_d: float) -> float:
        """
        Calcula score baseado no Stochastic RSI
        
        Args:
            stoch_k: Valor do Stochastic RSI %K
            stoch_d: Valor do Stochastic RSI %D
            
        Returns:
            Score entre -1 (oversold) e 1 (overbought)
        """
        if stoch_k is None:
            return 0.0
        
        score = 0.0
        
        # Stochastic abaixo de 20 é oversold (sinal de compra)
        if stoch_k <= 20:
            score += -0.5
        # Stochastic acima de 80 é overbought (sinal de venda)
        elif stoch_k >= 80:
            score += 0.5
        else:
            # Neutro, tendendo para onde está
            score += (stoch_k - 50) / 60
        
        # Cruzamento K > D é bullish
        if stoch_d is not None:
            if stoch_k > stoch_d:
                score += 0.3
            else:
                score -= 0.3
        
        return max(-1.0, min(1.0, score))
    
    @staticmethod
    def _calculate_adx_score(adx: float) -> float:
        """
        Calcula score baseado no ADX (força da tendência)
        
        Args:
            adx: Valor do ADX
            
        Returns:
            Score entre 0 (sem tendência) e 1 (tendência forte)
        """
        if adx is None:
            return 0.5
        
        # ADX não indica direção, apenas força
        # Quanto maior, mais forte a tendência (seja alta ou baixa)
        if adx >= 25:
            return 1.0  # Tendência forte
        elif adx >= 20:
            return 0.75  # Tendência moderada
        else:
            return 0.5  # Tendência fraca/sem tendência
    
    @staticmethod
    def _calculate_mfi_score(mfi: float) -> float:
        """
        Calcula score baseado no MFI (Money Flow Index)
        
        Args:
            mfi: Valor do MFI
            
        Returns:
            Score entre -1 (oversold) e 1 (overbought)
        """
        if mfi is None:
            return 0.0
        
        if mfi <= 20:
            # Oversold - sinal de compra
            return -1.0 + (mfi / 20) * 0.5
        elif mfi >= 80:
            # Overbought - sinal de venda
            return 1.0 - ((100 - mfi) / 20) * 0.5
        else:
            # Neutro
            return (mfi - 50) / 60
    
    @staticmethod
    def _calculate_bollinger_score(close: float, bb_upper: float, bb_middle: float, bb_lower: float) -> float:
        """
        Calcula score baseado nas Bandas de Bollinger
        
        Args:
            close: Preço de fechamento
            bb_upper: Banda superior
            bb_middle: Banda média
            bb_lower: Banda inferior
            
        Returns:
            Score entre -1 (na banda inferior) e 1 (na banda superior)
        """
        if bb_upper is None or bb_middle is None or bb_lower is None:
            return 0.0
        
        # Posição do preço nas bandas
        if close >= bb_upper:
            return 1.0  # Sobrecompra
        elif close <= bb_lower:
            return -1.0  # Sobrevenda
        else:
            # Normaliza posição entre as bandas
            band_range = bb_upper - bb_lower
            if band_range == 0:
                return 0.0
            position = (close - bb_lower) / band_range
            return (position - 0.5) * 2  # Converte 0-1 para -1 a 1
    
    @staticmethod
    def _calculate_atr_score(atr: float, close: float) -> float:
        """
        Calcula score baseado no ATR (volatilidade)
        
        Args:
            atr: Valor do ATR
            close: Preço de fechamento
            
        Returns:
            Score entre 0 (baixa volatilidade) e 1 (alta volatilidade)
        """
        if atr is None or close is None or close == 0:
            return 0.5
        
        # ATR como porcentagem do preço
        atr_percent = (atr / close) * 100
        
        # Alta volatilidade (>3%) = 1.0, Baixa volatilidade (<1%) = 0.0
        if atr_percent >= 3:
            return 1.0
        elif atr_percent <= 1:
            return 0.0
        else:
            return (atr_percent - 1) / 2
    
    @staticmethod
    def calculate_overall_score(indicators: Dict[str, Any], last_close: float, current_volume: float) -> float:
        """
        Calcula score geral baseado em todos os indicadores com pesos específicos:
        - Tendência (EMAs, ADX): 40%
        - Momento (RSI, MACD, Stochastic): 30%
        - Volume e volatilidade (MFI, ATR, Bollinger): 20%
        - Sentimento (neutro): 10%
        
        Args:
            indicators: Dicionário com todos os indicadores (novo formato ou antigo)
            last_close: Último preço de fechamento
            current_volume: Volume atual
            
        Returns:
            Score entre 0.0 e 1.0 (0 = muito baixista, 1 = muito altista)
        """
        # Valida dados de entrada
        if not indicators or last_close is None or last_close <= 0:
            return 0.5  # Retorna neutro se dados inválidos
        
        # Converte para formato flat se necessário
        flat_indicators = ScoreEngine._flatten_indicators(indicators)
        
        # ========== TENDÊNCIA (40%) ==========
        ema_score = ScoreEngine._calculate_ema_score(
            last_close,
            flat_indicators.get('ema9'),
            flat_indicators.get('ema21'),
            flat_indicators.get('ema200')
        )
        
        adx = flat_indicators.get('adx')
        adx_strength = ScoreEngine._calculate_adx_score(adx)
        
        # ADX modifica o peso da EMA: se tendência forte, aumenta importância
        # EMA score está em -1 a 1, ADX strength em 0 a 1
        # Combinamos: se EMA positiva e ADX forte = mais bullish
        #              se EMA negativa e ADX forte = mais bearish
        trend_score = ema_score * (0.7 + 0.3 * adx_strength)  # -1 a 1
        
        # ========== MOMENTO (30%) ==========
        rsi_score = ScoreEngine._calculate_rsi_score(flat_indicators.get('rsi'))
        macd_score = ScoreEngine._calculate_macd_score(
            flat_indicators.get('macd'),
            flat_indicators.get('macd_signal'),
            flat_indicators.get('macd_histogram')
        )
        stoch_score = ScoreEngine._calculate_stochastic_score(
            flat_indicators.get('stoch_rsi_k'),
            flat_indicators.get('stoch_rsi_d')
        )
        
        # Média ponderada dos indicadores de momento
        momentum_score = (rsi_score * 0.4 + macd_score * 0.4 + stoch_score * 0.2)  # -1 a 1
        
        # ========== VOLUME E VOLATILIDADE (20%) ==========
        mfi_score = ScoreEngine._calculate_mfi_score(flat_indicators.get('mfi'))
        
        bb_score = ScoreEngine._calculate_bollinger_score(
            last_close,
            flat_indicators.get('bb_upper'),
            flat_indicators.get('bb_middle'),
            flat_indicators.get('bb_lower')
        )
        
        atr_strength = ScoreEngine._calculate_atr_score(
            flat_indicators.get('atr'),
            last_close
        )
        
        volume_score = ScoreEngine._calculate_volume_score(
            current_volume if current_volume else 0,
            flat_indicators.get('volume_ma')
        )
        # Normaliza volume para -1 a 1
        volume_normalized = (volume_score - 0.5) * 2
        
        # Combina: MFI (30%), Bollinger (30%), Volume (30%), ATR como modificador (10%)
        vol_volatility_score = (
            mfi_score * 0.3 + 
            bb_score * 0.3 + 
            volume_normalized * 0.3 * (0.8 + 0.2 * atr_strength)
        )  # -1 a 1
        
        # ========== SENTIMENTO (10%) ==========
        # Por enquanto neutro (0.0)
        sentiment_score = 0.0
        
        # ========== SCORE FINAL PONDERADO ==========
        # Todos os scores estão em -1 a 1
        weighted_score = (
            trend_score * 0.40 +
            momentum_score * 0.30 +
            vol_volatility_score * 0.20 +
            sentiment_score * 0.10
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
            indicators: Dicionário com indicadores (novo formato ou antigo)
            
        Returns:
            String com diagnóstico:
            >= 0.7 → "Alta probabilidade de alta"
            0.4–0.69 → "Tendência neutra com leve viés de alta"
            < 0.4 → "Baixa probabilidade de alta / possível queda"
        """
        if score >= 0.7:
            return "Alta probabilidade de alta"
        elif score >= 0.4:
            return "Tendência neutra com leve viés de alta"
        else:
            return "Baixa probabilidade de alta / possível queda"
    
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
    
    @staticmethod
    def analyze_short_term_opportunity(indicators_1h: Dict[str, Any], last_close: float, current_volume: float) -> Dict[str, Any]:
        """
        Analisa oportunidades de trade rápido (day trade / scalp) no timeframe de 1h
        Usa os mesmos pesos do score geral:
        - Tendência (EMAs, ADX): 40%
        - Momento (RSI, MACD, Stochastic): 30%
        - Volume e volatilidade (MFI, ATR, Bollinger): 20%
        - Sentimento: 10%
        
        Args:
            indicators_1h: Indicadores do timeframe 1h
            last_close: Último preço de fechamento
            current_volume: Volume atual
            
        Returns:
            Dicionário com probabilidade (0-1) e comentário
        """
        # Usa o mesmo cálculo de score geral
        probability = ScoreEngine.calculate_overall_score(indicators_1h, last_close, current_volume)
        
        # Gera comentário baseado na probabilidade com as faixas especificadas
        if probability >= 0.7:
            comment = "Alta probabilidade de alta"
        elif probability >= 0.4:
            comment = "Tendência neutra com leve viés de alta"
        else:
            comment = "Baixa probabilidade de alta / possível queda"
        
        return {
            'probability': probability,
            'comment': comment
        }

