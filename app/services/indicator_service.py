"""
Serviço para calcular indicadores técnicos
"""
import pandas as pd
import pandas_ta as ta
from typing import Dict, Any


class IndicatorService:
    """Serviço para cálculo de indicadores técnicos"""
    
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

