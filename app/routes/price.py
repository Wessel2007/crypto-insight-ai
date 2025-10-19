"""
Rotas para consulta de preços
"""
from fastapi import APIRouter, HTTPException
from app.services.crypto_service import CryptoService
from app.models.schemas import PriceResponse, CandleData
from app.routes.helpers import validate_and_normalize_symbol, handle_crypto_service_error

router = APIRouter()
crypto_service = CryptoService()


@router.get("/price/{symbol}", response_model=PriceResponse)
async def get_price(symbol: str):
    """
    Busca os últimos candles de uma criptomoeda em múltiplos timeframes
    
    Args:
        symbol: Símbolo da moeda (BTC, ETH, SOL)
        
    Returns:
        Dados dos candles em 1h, 4h e 1d
    """
    try:
        # Valida e normaliza o símbolo
        normalized_symbol = validate_and_normalize_symbol(symbol, crypto_service)
        
        # Busca dados dos timeframes
        timeframes = ['1h', '4h', '1d']
        try:
            data = crypto_service.get_multiple_timeframes(normalized_symbol, timeframes, limit=500)
        except Exception as e:
            handle_crypto_service_error(e, symbol, "buscar dados")
        
        # Formata resposta
        result = {
            "symbol": normalized_symbol,
            "timeframes": {}
        }
        
        for tf, df in data.items():
            candles = []
            for _, row in df.iterrows():
                candle = CandleData(
                    timestamp=int(row['timestamp'].timestamp() * 1000),
                    open=float(row['open']),
                    high=float(row['high']),
                    low=float(row['low']),
                    close=float(row['close']),
                    volume=float(row['volume'])
                )
                candles.append(candle)
            
            result["timeframes"][tf] = candles
        
        return result
        
    except HTTPException:
        # Re-lança HTTPExceptions que já foram tratadas
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Dados inválidos: {str(e)}")
    except Exception as e:
        # Log do erro (em produção deveria usar logging adequado)
        print(f"❌ Erro não tratado em /price/{symbol}: {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor. Tente novamente.")

