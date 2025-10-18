"""
Serviço para calcular indicadores técnicos
"""
import pandas as pd
import pandas_ta as ta
from typing import Dict, Any


class IndicatorService:
    """Serviço para cálculo de indicadores técnicos"""
    
    @staticmethod
    def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calcula o RSI (Relative Strength Index)
        
        Args:
            df: DataFrame com dados OHLCV
            period: Período para o cálculo (padrão 14)
            
        Returns:
            Series com valores do RSI
        """
        return ta.rsi(df['close'], length=period)
    
    @staticmethod
    def calculate_ema(df: pd.DataFrame, period: int) -> pd.Series:
        """
        Calcula a EMA (Exponential Moving Average)
        
        Args:
            df: DataFrame com dados OHLCV
            period: Período para o cálculo
            
        Returns:
            Series com valores da EMA
        """
        return ta.ema(df['close'], length=period)
    
    @staticmethod
    def calculate_volume_ma(df: pd.DataFrame, period: int = 20) -> pd.Series:
        """
        Calcula a média móvel do volume
        
        Args:
            df: DataFrame com dados OHLCV
            period: Período para o cálculo (padrão 20)
            
        Returns:
            Series com valores da média de volume
        """
        return ta.sma(df['volume'], length=period)
    
    @staticmethod
    def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        Calcula o MACD (Moving Average Convergence Divergence)
        
        Args:
            df: DataFrame com dados OHLCV
            fast: Período rápido (padrão 12)
            slow: Período lento (padrão 26)
            signal: Período do sinal (padrão 9)
            
        Returns:
            DataFrame com MACD, Signal e Histogram
        """
        macd = df.ta.macd(close='close', fast=fast, slow=slow, signal=signal)
        return macd
    
    @staticmethod
    def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calcula o ATR (Average True Range)
        
        Args:
            df: DataFrame com dados OHLCV
            period: Período para o cálculo (padrão 14)
            
        Returns:
            Series com valores do ATR
        """
        return ta.atr(df['high'], df['low'], df['close'], length=period)
    
    @staticmethod
    def _safe_float(series: pd.Series, decimals: int = 2):
        """
        Converte série pandas para float com tratamento de NaN e arredondamento
        
        Args:
            series: Série pandas
            decimals: Número de casas decimais
            
        Returns:
            Float arredondado ou None se inválido
        """
        if series is None or len(series) == 0:
            return None
        value = series.iloc[-1]
        if pd.isna(value):
            return None
        return round(float(value), decimals)
    
    @staticmethod
    def get_indicators(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcula todos os indicadores técnicos e retorna em formato JSON pronto para API
        
        Args:
            df: DataFrame com dados OHLCV (colunas: timestamp, open, high, low, close, volume)
            
        Returns:
            Dicionário com indicadores formatados:
            - rsi: RSI (14)
            - ema9, ema21, ema200: Médias Móveis Exponenciais
            - macd: MACD line
            - macd_signal: MACD signal line
            - macd_histogram: MACD histogram
            - volume_ma: Média móvel de volume (20 períodos)
            - atr: Average True Range (14)
            - last_close: Último preço de fechamento
            - current_volume: Volume atual
        """
        # Valida se há dados suficientes
        if df is None or df.empty or len(df) < 14:
            return {
                'rsi': None,
                'ema9': None,
                'ema21': None,
                'ema200': None,
                'macd': None,
                'macd_signal': None,
                'macd_histogram': None,
                'volume_ma': None,
                'atr': None,
                'last_close': None,
                'current_volume': None
            }
        
        # Valida colunas necessárias
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"DataFrame faltando colunas: {', '.join(missing_columns)}")
        
        # Calcula RSI (14)
        rsi = ta.rsi(df['close'], length=14)
        
        # Calcula EMAs
        ema9 = ta.ema(df['close'], length=9)
        ema21 = ta.ema(df['close'], length=21)
        ema200 = ta.ema(df['close'], length=200) if len(df) >= 200 else None
        
        # Calcula MACD (12, 26, 9)
        macd_df = df.ta.macd(close='close', fast=12, slow=26, signal=9)
        
        # Calcula Média de Volume (20 períodos)
        volume_ma = ta.sma(df['volume'], length=20)
        
        # Calcula ATR (14)
        atr = ta.atr(df['high'], df['low'], df['close'], length=14)
        
        # Monta o dicionário de resposta usando a função auxiliar
        indicators = {
            # RSI (2 casas decimais)
            'rsi': IndicatorService._safe_float(rsi, 2),
            
            # EMAs (2 casas decimais)
            'ema9': IndicatorService._safe_float(ema9, 2),
            'ema21': IndicatorService._safe_float(ema21, 2),
            'ema200': IndicatorService._safe_float(ema200, 2) if ema200 is not None else None,
            
            # MACD (4 casas decimais para precisão)
            'macd': IndicatorService._safe_float(macd_df['MACD_12_26_9'], 4) if 'MACD_12_26_9' in macd_df.columns else None,
            'macd_signal': IndicatorService._safe_float(macd_df['MACDs_12_26_9'], 4) if 'MACDs_12_26_9' in macd_df.columns else None,
            'macd_histogram': IndicatorService._safe_float(macd_df['MACDh_12_26_9'], 4) if 'MACDh_12_26_9' in macd_df.columns else None,
            
            # Volume (2 casas decimais)
            'volume_ma': IndicatorService._safe_float(volume_ma, 2),
            
            # ATR (2 casas decimais)
            'atr': IndicatorService._safe_float(atr, 2),
            
            # Dados extras
            'last_close': IndicatorService._safe_float(df['close'], 2),
            'current_volume': IndicatorService._safe_float(df['volume'], 2)
        }
        
        return indicators
    
    @staticmethod
    def get_indicators_summary(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Retorna um resumo dos indicadores com interpretação básica
        
        Args:
            df: DataFrame com dados OHLCV
            
        Returns:
            Dicionário com indicadores e interpretação
        """
        # Reutiliza get_indicators que já faz tudo
        return IndicatorService.get_indicators(df)

