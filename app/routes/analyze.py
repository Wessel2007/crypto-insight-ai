"""
Rotas para análise técnica
"""
from fastapi import APIRouter, HTTPException
from app.services.crypto_service import CryptoService
from app.services.indicator_service import IndicatorService
from app.utils.score_engine import ScoreEngine
from app.utils.ai_analyzer import generate_ai_comment
from app.models.schemas import AnalyzeResponse, IndicatorData

router = APIRouter()
crypto_service = CryptoService()
indicator_service = IndicatorService()
score_engine = ScoreEngine()


@router.get("/analyze/{symbol}", response_model=AnalyzeResponse)
async def analyze_symbol(symbol: str):
    """
    Analisa uma criptomoeda e retorna indicadores técnicos e score
    
    Args:
        symbol: Símbolo da moeda (BTC, ETH, SOL)
        
    Returns:
        Análise técnica completa com indicadores, score e diagnóstico
    """
    try:
        # Valida símbolo
        if not symbol or len(symbol) > 20:
            raise HTTPException(status_code=400, detail="Símbolo inválido")
        
        # Normaliza o símbolo
        try:
            normalized_symbol = crypto_service.normalize_symbol(symbol)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao normalizar símbolo: {str(e)}")
        
        # Busca dados dos timeframes
        timeframes = ['1h', '4h', '1d']
        try:
            data = crypto_service.get_multiple_timeframes(normalized_symbol, timeframes, limit=500)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            error_msg = str(e).lower()
            if 'network' in error_msg or 'timeout' in error_msg:
                raise HTTPException(status_code=503, detail=f"Erro de conexão com a exchange: {str(e)}")
            elif 'exchange' in error_msg:
                raise HTTPException(status_code=400, detail=f"Erro da exchange: {str(e)}")
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao buscar dados: {str(e)}")
        
        # Calcula indicadores para cada timeframe
        timeframes_data = {}
        indicators_response = {}
        
        for tf, df in data.items():
            # Calcula todos os indicadores usando a nova função get_indicators
            indicators = indicator_service.get_indicators(df)
            
            # Prepara dados para o score engine
            timeframes_data[tf] = {
                'indicators': indicators,
                'last_close': indicators.get('last_close'),
                'current_volume': indicators.get('current_volume')
            }
            
            # Formata indicadores para resposta
            indicators_response[tf] = IndicatorData(
                rsi=indicators.get('rsi'),
                ema9=indicators.get('ema9'),
                ema21=indicators.get('ema21'),
                ema200=indicators.get('ema200'),
                volume_ma=indicators.get('volume_ma'),
                macd=indicators.get('macd'),
                macd_signal=indicators.get('macd_signal'),
                macd_histogram=indicators.get('macd_histogram'),
                atr=indicators.get('atr')
            )
        
        # Analisa múltiplos timeframes e calcula score
        analysis = score_engine.analyze_multiple_timeframes(timeframes_data)
        
        # Gera comentário natural usando IA
        # Usa os indicadores do timeframe diário (mais relevante)
        daily_indicators = timeframes_data.get('1d', {}).get('indicators', {})
        symbol_name = symbol.upper()  # Ex: "BTC" -> "Bitcoin" seria ideal, mas usamos o símbolo
        
        ai_comment = generate_ai_comment(
            indicators=daily_indicators,
            score=analysis['overall_score'],
            symbol=symbol_name,
            news=None  # Pode ser integrado com news_fetcher futuramente
        )
        
        # Prepara resposta
        response = AnalyzeResponse(
            symbol=normalized_symbol,
            timeframes=timeframes,
            indicators=indicators_response,
            score=analysis['overall_score'],
            diagnostic=analysis['overall_diagnostic'],
            ai_comment=ai_comment
        )
        
        return response
        
    except HTTPException:
        # Re-lança HTTPExceptions que já foram tratadas
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Dados inválidos: {str(e)}")
    except Exception as e:
        # Log do erro (em produção deveria usar logging adequado)
        print(f"❌ Erro não tratado em /analyze/{symbol}: {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor. Tente novamente.")

