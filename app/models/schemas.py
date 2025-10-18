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


class IndicatorData(BaseModel):
    """Dados de indicadores técnicos"""
    rsi: Optional[float] = None
    ema9: Optional[float] = None
    ema21: Optional[float] = None
    ema200: Optional[float] = None
    volume_ma: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    atr: Optional[float] = None


class TimeframeIndicators(BaseModel):
    """Indicadores por timeframe"""
    timeframe: str
    indicators: IndicatorData
    last_close: float


class AnalyzeResponse(BaseModel):
    """Resposta do endpoint /analyze/{symbol}"""
    symbol: str
    timeframes: List[str]
    indicators: Dict[str, IndicatorData]
    score: float
    diagnostic: str
    ai_comment: Optional[str] = None


class HealthResponse(BaseModel):
    """Resposta do endpoint raiz"""
    status: str

