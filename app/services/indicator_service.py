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
    def calculate_sma(df: pd.DataFrame, period: int) -> pd.Series:
        """
        Calcula a SMA (Simple Moving Average)
        
        Args:
            df: DataFrame com dados OHLCV
            period: Período para o cálculo
            
        Returns:
            Series com valores da SMA
        """
        return ta.sma(df['close'], length=period)
    
    @staticmethod
    def calculate_bollinger_bands(df: pd.DataFrame, period: int = 20, std: int = 2) -> pd.DataFrame:
        """
        Calcula as Bandas de Bollinger
        
        Args:
            df: DataFrame com dados OHLCV
            period: Período para o cálculo (padrão 20)
            std: Desvio padrão (padrão 2)
            
        Returns:
            DataFrame com upper, middle e lower bands
        """
        return ta.bbands(df['close'], length=period, std=std)
    
    @staticmethod
    def calculate_adx(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        Calcula o ADX (Average Directional Index)
        
        Args:
            df: DataFrame com dados OHLCV
            period: Período para o cálculo (padrão 14)
            
        Returns:
            DataFrame com ADX, DMP e DMN
        """
        return ta.adx(df['high'], df['low'], df['close'], length=period)
    
    @staticmethod
    def calculate_stoch_rsi(df: pd.DataFrame, length: int = 14, rsi_length: int = 14, k: int = 3, d: int = 3) -> pd.DataFrame:
        """
        Calcula o Stochastic RSI
        
        Args:
            df: DataFrame com dados OHLCV
            length: Período do Stochastic (padrão 14)
            rsi_length: Período do RSI (padrão 14)
            k: Período do %K (padrão 3)
            d: Período do %D (padrão 3)
            
        Returns:
            DataFrame com STOCHRSIk e STOCHRSId
        """
        return ta.stochrsi(df['close'], length=length, rsi_length=rsi_length, k=k, d=d)
    
    @staticmethod
    def calculate_mfi(df: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calcula o MFI (Money Flow Index)
        
        Args:
            df: DataFrame com dados OHLCV
            period: Período para o cálculo (padrão 14)
            
        Returns:
            Series com valores do MFI
        """
        return ta.mfi(df['high'], df['low'], df['close'], df['volume'], length=period)
    
    @staticmethod
    def calculate_obv(df: pd.DataFrame) -> pd.Series:
        """
        Calcula o OBV (On Balance Volume)
        
        Args:
            df: DataFrame com dados OHLCV
            
        Returns:
            Series com valores do OBV
        """
        return ta.obv(df['close'], df['volume'])
    
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
            Dicionário com indicadores organizados por categoria:
            - trend: EMA9, EMA21, EMA50, EMA200, SMA100
            - momentum: RSI, Stochastic_RSI, MACD
            - volatility: ATR, Bollinger_Bands
            - volume: Volume_MA, MFI, OBV
            - strength: ADX
            - price: last_close, current_volume
        """
        # Valida se há dados suficientes
        if df is None or df.empty or len(df) < 14:
            return {
                'trend': {
                    'EMA9': None,
                    'EMA21': None,
                    'EMA50': None,
                    'EMA200': None,
                    'SMA100': None
                },
                'momentum': {
                    'RSI': None,
                    'Stochastic_RSI_K': None,
                    'Stochastic_RSI_D': None,
                    'MACD': None,
                    'MACD_Signal': None,
                    'MACD_Histogram': None
                },
                'volatility': {
                    'ATR': None,
                    'BB_Upper': None,
                    'BB_Middle': None,
                    'BB_Lower': None
                },
                'volume': {
                    'Volume_MA': None,
                    'MFI': None,
                    'OBV': None
                },
                'strength': {
                    'ADX': None
                },
                'price': {
                    'last_close': None,
                    'current_volume': None
                }
            }
        
        # Valida colunas necessárias
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"DataFrame faltando colunas: {', '.join(missing_columns)}")
        
        # ========== INDICADORES DE TENDÊNCIA (TREND) ==========
        ema9 = ta.ema(df['close'], length=9)
        ema21 = ta.ema(df['close'], length=21)
        ema50 = ta.ema(df['close'], length=50) if len(df) >= 50 else None
        ema200 = ta.ema(df['close'], length=200) if len(df) >= 200 else None
        sma100 = ta.sma(df['close'], length=100) if len(df) >= 100 else None
        
        # ========== INDICADORES DE MOMENTUM ==========
        rsi = ta.rsi(df['close'], length=14)
        
        # Stochastic RSI (14, 14, 3, 3)
        stoch_rsi = ta.stochrsi(df['close'], length=14, rsi_length=14, k=3, d=3)
        
        # MACD (12, 26, 9)
        macd_df = df.ta.macd(close='close', fast=12, slow=26, signal=9)
        
        # ========== INDICADORES DE VOLATILIDADE ==========
        atr = ta.atr(df['high'], df['low'], df['close'], length=14)
        
        # Bollinger Bands (20, 2)
        bb = ta.bbands(df['close'], length=20, std=2)
        
        # ========== INDICADORES DE VOLUME ==========
        volume_ma = ta.sma(df['volume'], length=20)
        mfi = ta.mfi(df['high'], df['low'], df['close'], df['volume'], length=14)
        obv = ta.obv(df['close'], df['volume'])
        
        # ========== INDICADORES DE FORÇA ==========
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        
        # Monta o dicionário de resposta organizado por categorias
        indicators = {
            'trend': {
                'EMA9': IndicatorService._safe_float(ema9, 2),
                'EMA21': IndicatorService._safe_float(ema21, 2),
                'EMA50': IndicatorService._safe_float(ema50, 2) if ema50 is not None else None,
                'EMA200': IndicatorService._safe_float(ema200, 2) if ema200 is not None else None,
                'SMA100': IndicatorService._safe_float(sma100, 2) if sma100 is not None else None
            },
            'momentum': {
                'RSI': IndicatorService._safe_float(rsi, 2),
                'Stochastic_RSI_K': IndicatorService._safe_float(stoch_rsi[f'STOCHRSIk_14_14_3_3'], 2) if f'STOCHRSIk_14_14_3_3' in stoch_rsi.columns else None,
                'Stochastic_RSI_D': IndicatorService._safe_float(stoch_rsi[f'STOCHRSId_14_14_3_3'], 2) if f'STOCHRSId_14_14_3_3' in stoch_rsi.columns else None,
                'MACD': IndicatorService._safe_float(macd_df['MACD_12_26_9'], 4) if 'MACD_12_26_9' in macd_df.columns else None,
                'MACD_Signal': IndicatorService._safe_float(macd_df['MACDs_12_26_9'], 4) if 'MACDs_12_26_9' in macd_df.columns else None,
                'MACD_Histogram': IndicatorService._safe_float(macd_df['MACDh_12_26_9'], 4) if 'MACDh_12_26_9' in macd_df.columns else None
            },
            'volatility': {
                'ATR': IndicatorService._safe_float(atr, 2),
                'BB_Upper': IndicatorService._safe_float(bb['BBU_20_2.0_2.0'], 2) if bb is not None and 'BBU_20_2.0_2.0' in bb.columns else None,
                'BB_Middle': IndicatorService._safe_float(bb['BBM_20_2.0_2.0'], 2) if bb is not None and 'BBM_20_2.0_2.0' in bb.columns else None,
                'BB_Lower': IndicatorService._safe_float(bb['BBL_20_2.0_2.0'], 2) if bb is not None and 'BBL_20_2.0_2.0' in bb.columns else None
            },
            'volume': {
                'Volume_MA': IndicatorService._safe_float(volume_ma, 2),
                'MFI': IndicatorService._safe_float(mfi, 2),
                'OBV': IndicatorService._safe_float(obv, 0)  # OBV geralmente sem casas decimais
            },
            'strength': {
                'ADX': IndicatorService._safe_float(adx_df['ADX_14'], 2) if 'ADX_14' in adx_df.columns else None
            },
            'price': {
                'last_close': IndicatorService._safe_float(df['close'], 2),
                'current_volume': IndicatorService._safe_float(df['volume'], 2)
            }
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
    
    @staticmethod
    def get_chart_data(df: pd.DataFrame, limit: int = 200) -> pd.DataFrame:
        """
        Retorna dados de candles com EMAs calculadas para gráfico
        
        Args:
            df: DataFrame com dados OHLCV
            limit: Número máximo de candles para retornar (últimos N candles)
            
        Returns:
            DataFrame com colunas: timestamp, open, high, low, close, volume, ema9, ema21, ema200
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        # Calcula as EMAs
        df_chart = df.copy()
        df_chart['ema9'] = ta.ema(df_chart['close'], length=9)
        df_chart['ema21'] = ta.ema(df_chart['close'], length=21)
        
        # EMA200 só se houver dados suficientes
        if len(df_chart) >= 200:
            df_chart['ema200'] = ta.ema(df_chart['close'], length=200)
        else:
            df_chart['ema200'] = None
        
        # Seleciona as colunas necessárias
        chart_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'ema9', 'ema21', 'ema200']
        df_chart = df_chart[chart_columns]
        
        # Retorna apenas os últimos N candles
        df_chart = df_chart.tail(limit)
        
        return df_chart

