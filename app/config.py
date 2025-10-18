"""
Configurações da aplicação Crypto Insight AI
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Configurações da aplicação
    
    As variáveis podem ser definidas em um arquivo .env
    """
    
    # Configurações da API
    app_name: str = "Crypto Insight AI"
    app_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Configurações da Exchange
    exchange_name: str = "binance"
    exchange_type: str = "spot"
    
    # Configurações dos Indicadores
    rsi_period: int = 14
    ema_fast: int = 9
    ema_medium: int = 21
    ema_slow: int = 200
    volume_ma_period: int = 20
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    
    # Configurações de Dados
    default_candle_limit: int = 100
    analysis_candle_limit: int = 200
    default_timeframes: list = ["1h", "4h", "1d"]
    
    # Configurações de CORS
    cors_origins: list = ["*"]
    
    # Ambiente
    environment: str = "development"
    debug: bool = True
    
    # API Keys (para expansões futuras)
    news_api_key: Optional[str] = None
    sentiment_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instância global das configurações
settings = Settings()

