"""
Rotas para análise técnica
"""
from fastapi import APIRouter, HTTPException
from app.services.crypto_service import CryptoService
from app.services.indicator_service import IndicatorService
from app.utils.score_engine import ScoreEngine
from app.utils.ai_analyzer import generate_ai_comment
from app.models.schemas import (
    AnalyzeResponse, IndicatorData, ChartDataResponse, CandleWithEMA,
    TrendIndicators, MomentumIndicators, VolatilityIndicators, 
    VolumeIndicators, StrengthIndicators, PriceData, TradeOpportunity
)
from app.routes.helpers import validate_and_normalize_symbol, handle_crypto_service_error
import pandas as pd

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
        # Valida e normaliza o símbolo
        normalized_symbol = validate_and_normalize_symbol(symbol, crypto_service)
        
        # Busca dados dos timeframes
        timeframes = ['1h', '4h', '1d']
        try:
            data = crypto_service.get_multiple_timeframes(normalized_symbol, timeframes, limit=500)
        except Exception as e:
            handle_crypto_service_error(e, symbol, "buscar dados")
        
        # Calcula indicadores para cada timeframe
        timeframes_data = {}
        indicators_response = {}
        
        for tf, df in data.items():
            # Calcula todos os indicadores usando a nova função get_indicators
            indicators = indicator_service.get_indicators(df)
            
            # Prepara dados para o score engine
            timeframes_data[tf] = {
                'indicators': indicators,
                'last_close': indicators['price'].get('last_close'),
                'current_volume': indicators['price'].get('current_volume')
            }
            
            # Formata indicadores para resposta usando a nova estrutura
            indicators_response[tf] = IndicatorData(
                trend=TrendIndicators(**indicators['trend']),
                momentum=MomentumIndicators(**indicators['momentum']),
                volatility=VolatilityIndicators(**indicators['volatility']),
                volume=VolumeIndicators(**indicators['volume']),
                strength=StrengthIndicators(**indicators['strength']),
                price=PriceData(**indicators['price'])
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
        
        # Analisa oportunidade de trade rápido (timeframe 1h)
        trade_opportunity = None
        hourly_data = timeframes_data.get('1h')
        if hourly_data:
            trade_analysis = score_engine.analyze_short_term_opportunity(
                indicators_1h=hourly_data.get('indicators', {}),
                last_close=hourly_data.get('last_close', 0),
                current_volume=hourly_data.get('current_volume', 0)
            )
            trade_opportunity = TradeOpportunity(
                probability=trade_analysis['probability'],
                comment=trade_analysis['comment']
            )
        
        # Prepara dados do gráfico (timeframe de 4h com 200 candles)
        chart_data = None
        try:
            # Usa dados de 4h para o gráfico (bom equilíbrio entre detalhe e visão geral)
            df_chart = data.get('4h')
            if df_chart is not None and not df_chart.empty:
                chart_df = indicator_service.get_chart_data(df_chart, limit=200)
                
                # Converte para lista de CandleWithEMA
                candles_list = []
                for _, row in chart_df.iterrows():
                    candle = CandleWithEMA(
                        time=int(row['timestamp'].timestamp()),  # Converte para timestamp Unix
                        open=float(row['open']),
                        high=float(row['high']),
                        low=float(row['low']),
                        close=float(row['close']),
                        volume=float(row['volume']),
                        ema9=float(row['ema9']) if pd.notna(row['ema9']) else None,
                        ema21=float(row['ema21']) if pd.notna(row['ema21']) else None,
                        ema200=float(row['ema200']) if pd.notna(row['ema200']) else None
                    )
                    candles_list.append(candle)
                
                chart_data = ChartDataResponse(
                    symbol=normalized_symbol,
                    timeframe='4h',
                    candles=candles_list
                )
        except Exception as e:
            # Se houver erro ao preparar dados do gráfico, apenas loga mas não falha a análise
            print(f"⚠️ Erro ao preparar dados do gráfico: {str(e)}")
        
        # Prepara resposta
        response = AnalyzeResponse(
            symbol=normalized_symbol,
            timeframes=timeframes,
            indicators=indicators_response,
            score=analysis['overall_score'],
            diagnostic=analysis['overall_diagnostic'],
            ai_comment=ai_comment,
            chart_data=chart_data,
            trade_opportunity=trade_opportunity
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

