"""
Serviço para buscar dados de criptomoedas usando CCXT
"""
import ccxt
import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime, timezone
import pytz
import time


class CryptoService:
    """Serviço para interagir com exchanges de cripto"""
    
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        """
        Inicializa a exchange (Binance por padrão)
        
        Args:
            max_retries: Número máximo de tentativas em caso de falha
            retry_delay: Delay entre tentativas (em segundos)
        """
        try:
            self.exchange = ccxt.binance({
                'enableRateLimit': True,
                'timeout': 10000,  # 10 segundos de timeout
                'options': {
                    'defaultType': 'spot'
                }
            })
            self.max_retries = max_retries
            self.retry_delay = retry_delay
        except Exception as e:
            raise Exception(f"Erro ao inicializar exchange: {str(e)}")
    
    def get_candles(self, symbol: str, timeframe: str = '1h', limit: int = 500) -> pd.DataFrame:
        """
        Busca candles de uma criptomoeda com retry automático
        SEMPRE busca dados em tempo real diretamente da API sem cache
        
        Args:
            symbol: Par de trading (ex: 'BTC/USDT')
            timeframe: Timeframe dos candles ('1h', '4h', '1d')
            limit: Número de candles para buscar (mínimo 500 recomendado)
            
        Returns:
            DataFrame com os dados dos candles (timestamp, open, high, low, close, volume)
            
        Raises:
            Exception: Se houver erro após todas as tentativas
        """
        # Valida parâmetros
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Símbolo inválido")
        
        if limit < 1 or limit > 1000:
            raise ValueError("Limite deve estar entre 1 e 1000")
        
        valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']
        if timeframe not in valid_timeframes:
            raise ValueError(f"Timeframe inválido. Use um dos: {', '.join(valid_timeframes)}")
        
        # Calcula o timestamp 'since' para garantir dados mais recentes
        # Usa exchange.milliseconds() para garantir sincronização com a exchange
        timeframe_minutes = {
            '1m': 1, '5m': 5, '15m': 15, '30m': 30,
            '1h': 60, '4h': 240, '1d': 1440, '1w': 10080
        }
        minutes = timeframe_minutes.get(timeframe, 60)
        
        # Usa o horário da exchange (mais preciso que time.time())
        now = self.exchange.milliseconds()
        # Calcula 'since' baseado no número de candles e timeframe
        # Fórmula: agora - (limit * intervalo_em_minutos * 60_segundos * 1000_milissegundos)
        since = now - (limit * minutes * 60 * 1000)
        
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                # Busca os dados da exchange COM parâmetro 'since' para garantir dados atualizados
                ohlcv = self.exchange.fetch_ohlcv(
                    symbol=symbol,
                    timeframe=timeframe,
                    since=since,
                    limit=limit
                )
                
                # Valida se recebeu dados
                if not ohlcv or len(ohlcv) == 0:
                    raise Exception(f"Nenhum dado retornado para {symbol}")
                
                # Converte para DataFrame
                df = pd.DataFrame(
                    ohlcv, 
                    columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
                )
                
                # Valida DataFrame
                if df.empty:
                    raise Exception(f"DataFrame vazio para {symbol}")
                
                # Guarda o timestamp do último candle ANTES de converter
                last_candle_timestamp_ms = df['timestamp'].iloc[-1]
                
                # Converte timestamp para datetime ANTES de retornar
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
                
                # Valida se o último candle é recente (dentro de 24h para timeframes maiores)
                max_delay_hours = {'1m': 1, '5m': 1, '15m': 2, '30m': 2, '1h': 3, '4h': 12, '1d': 48, '1w': 168}
                max_delay = max_delay_hours.get(timeframe, 24) * 60 * 60 * 1000  # em milissegundos
                
                if (now - last_candle_timestamp_ms) > max_delay:
                    print(f"⚠️ AVISO: Último candle de {symbol} ({timeframe}) está defasado!")
                    print(f"   Horário atual: {datetime.fromtimestamp(now/1000, tz=timezone.utc)}")
                    print(f"   Último candle: {datetime.fromtimestamp(last_candle_timestamp_ms/1000, tz=timezone.utc)}")
                
                return df
                
            except ccxt.NetworkError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))  # Backoff exponencial
                    continue
                raise Exception(f"Erro de rede ao buscar {symbol} após {self.max_retries} tentativas: {str(e)}")
            
            except ccxt.ExchangeError as e:
                # Erros da exchange não devem fazer retry
                raise Exception(f"Erro da exchange para {symbol}: {str(e)}")
            
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise Exception(f"Erro ao buscar dados de {symbol}: {str(e)}")
        
        # Se chegou aqui, todas as tentativas falharam
        raise Exception(f"Erro ao buscar dados de {symbol} após {self.max_retries} tentativas: {str(last_exception)}")
    
    def get_multiple_timeframes(self, symbol: str, timeframes: List[str] = None, limit: int = 500) -> Dict[str, pd.DataFrame]:
        """
        Busca candles de múltiplos timeframes
        
        Args:
            symbol: Par de trading (ex: 'BTC/USDT')
            timeframes: Lista de timeframes ('1h', '4h', '1d')
            limit: Número de candles para buscar em cada timeframe
            
        Returns:
            Dicionário com DataFrames por timeframe
        """
        if timeframes is None:
            timeframes = ['1h', '4h', '1d']
        
        result = {}
        for tf in timeframes:
            result[tf] = self.get_candles(symbol, tf, limit)
        
        return result
    
    def get_last_candle_timestamps(self, df: pd.DataFrame) -> Tuple[str, str]:
        """
        Extrai e formata os timestamps do último candle (UTC e Brasília)
        
        Args:
            df: DataFrame com os candles (coluna 'timestamp' já convertida para datetime)
            
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
    
    def normalize_symbol(self, symbol: str) -> str:
        """
        Normaliza o símbolo da moeda para o formato esperado
        
        Args:
            symbol: Símbolo da moeda (BTC, ETH, SOL)
            
        Returns:
            Símbolo normalizado (BTC/USDT, ETH/USDT, SOL/USDT)
        """
        symbol = symbol.upper()
        
        # Se já está no formato correto, retorna
        if '/' in symbol:
            return symbol
        
        # Adiciona /USDT se não tiver
        return f"{symbol}/USDT"
    
    def get_current_price(self, symbol: str) -> float:
        """
        Busca o preço atual de uma criptomoeda com retry
        
        Args:
            symbol: Par de trading (ex: 'BTC/USDT')
            
        Returns:
            Preço atual
            
        Raises:
            Exception: Se houver erro após todas as tentativas
        """
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Símbolo inválido")
        
        for attempt in range(self.max_retries):
            try:
                ticker = self.exchange.fetch_ticker(symbol)
                
                if not ticker or 'last' not in ticker:
                    raise Exception(f"Dados de ticker inválidos para {symbol}")
                
                price = ticker['last']
                
                if price is None or price <= 0:
                    raise Exception(f"Preço inválido para {symbol}: {price}")
                
                return float(price)
                
            except ccxt.NetworkError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise Exception(f"Erro de rede ao buscar preço de {symbol}: {str(e)}")
            
            except ccxt.ExchangeError as e:
                raise Exception(f"Erro da exchange para {symbol}: {str(e)}")
            
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                raise Exception(f"Erro ao buscar preço de {symbol}: {str(e)}")
        
        raise Exception(f"Erro ao buscar preço de {symbol} após {self.max_retries} tentativas")

