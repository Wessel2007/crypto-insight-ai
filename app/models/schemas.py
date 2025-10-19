"""
Schemas para validação de dados da API
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class CandleData(BaseModel):
    """Dados de um candle"""
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class PriceResponse(BaseModel):
    """Resposta do endpoint /price/{symbol}"""
    symbol: str
    timeframes: Dict[str, List[CandleData]]


class TrendIndicators(BaseModel):
    """Indicadores de Tendência"""
    EMA9: Optional[float] = None
    EMA21: Optional[float] = None
    EMA50: Optional[float] = None
    EMA200: Optional[float] = None
    SMA100: Optional[float] = None


class MomentumIndicators(BaseModel):
    """Indicadores de Momentum"""
    RSI: Optional[float] = None
    Stochastic_RSI_K: Optional[float] = None
    Stochastic_RSI_D: Optional[float] = None
    MACD: Optional[float] = None
    MACD_Signal: Optional[float] = None
    MACD_Histogram: Optional[float] = None


class VolatilityIndicators(BaseModel):
    """Indicadores de Volatilidade"""
    ATR: Optional[float] = None
    BB_Upper: Optional[float] = None
    BB_Middle: Optional[float] = None
    BB_Lower: Optional[float] = None


class VolumeIndicators(BaseModel):
    """Indicadores de Volume"""
    Volume_MA: Optional[float] = None
    MFI: Optional[float] = None
    OBV: Optional[float] = None


class StrengthIndicators(BaseModel):
    """Indicadores de Força"""
    ADX: Optional[float] = None


class PriceData(BaseModel):
    """Dados de Preço"""
    last_close: Optional[float] = None
    current_volume: Optional[float] = None


class IndicatorData(BaseModel):
    """Dados de indicadores técnicos organizados por categoria"""
    trend: TrendIndicators
    momentum: MomentumIndicators
    volatility: VolatilityIndicators
    volume: VolumeIndicators
    strength: StrengthIndicators
    price: PriceData


class TimeframeIndicators(BaseModel):
    """Indicadores por timeframe"""
    timeframe: str
    indicators: IndicatorData
    last_close: float


class CandleWithEMA(BaseModel):
    """Dados de um candle com EMAs calculadas"""
    time: int  # timestamp em segundos
    open: float
    high: float
    low: float
    close: float
    volume: float
    ema9: Optional[float] = None
    ema21: Optional[float] = None
    ema200: Optional[float] = None


class ChartDataResponse(BaseModel):
    """Resposta do endpoint /chart/{symbol}"""
    symbol: str
    timeframe: str
    candles: List[CandleWithEMA]


class TradeOpportunity(BaseModel):
    """Oportunidade de trade rápido (scalp/day trade)"""
    probability: float
    comment: str


class AnalyzeResponse(BaseModel):
    """Resposta do endpoint /analyze/{symbol}"""
    symbol: str
    timeframes: List[str]
    indicators: Dict[str, IndicatorData]
    score: float
    diagnostic: str
    ai_comment: Optional[str] = None
    chart_data: Optional[ChartDataResponse] = None
    trade_opportunity: Optional[TradeOpportunity] = None


class HealthResponse(BaseModel):
    """Resposta do endpoint raiz"""
    status: str

