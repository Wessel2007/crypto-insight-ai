"""
Exemplo de uso dos novos indicadores técnicos
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.crypto_service import CryptoService
from app.services.indicator_service import IndicatorService
import json


def analyze_with_new_indicators(symbol: str = "BTC/USDT"):
    """
    Demonstra o uso dos novos indicadores para análise técnica
    """
    print("=" * 80)
    print(f"ANALISE TECNICA COMPLETA: {symbol}")
    print("=" * 80)
    print()
    
    # Buscar dados
    print(f"[1/3] Buscando dados de {symbol}...")
    crypto = CryptoService()
    df = crypto.get_candles(symbol, timeframe='1h', limit=500)
    print(f"      OK - {len(df)} candles obtidos")
    print()
    
    # Calcular indicadores
    print("[2/3] Calculando todos os indicadores...")
    indicators = IndicatorService.get_indicators(df)
    print("      OK - 19 indicadores calculados")
    print()
    
    # Análise inteligente
    print("[3/3] Gerando analise...")
    print()
    
    # Obter valores
    trend = indicators['trend']
    momentum = indicators['momentum']
    volatility = indicators['volatility']
    volume = indicators['volume']
    strength = indicators['strength']
    price = indicators['price']
    
    print("=" * 80)
    print("ANALISE DE TENDENCIA")
    print("=" * 80)
    
    # Análise de EMAs
    current_price = price['last_close']
    ema9 = trend['EMA9']
    ema21 = trend['EMA21']
    ema50 = trend['EMA50']
    ema200 = trend['EMA200']
    sma100 = trend['SMA100']
    
    print(f"Preco Atual:  ${current_price:,.2f}")
    print(f"EMA9:         ${ema9:,.2f} {'(Acima)' if current_price > ema9 else '(Abaixo)'}")
    print(f"EMA21:        ${ema21:,.2f} {'(Acima)' if current_price > ema21 else '(Abaixo)'}")
    print(f"EMA50:        ${ema50:,.2f} {'(Acima)' if current_price > ema50 else '(Abaixo)'}")
    print(f"SMA100:       ${sma100:,.2f} {'(Acima)' if current_price > sma100 else '(Abaixo)'}")
    print(f"EMA200:       ${ema200:,.2f} {'(Acima)' if current_price > ema200 else '(Abaixo)'}")
    print()
    
    # Golden/Death Cross
    if ema9 > ema21:
        print("-> GOLDEN CROSS: EMA9 acima da EMA21 (ALTISTA)")
    else:
        print("-> DEATH CROSS: EMA9 abaixo da EMA21 (BAIXISTA)")
    print()
    
    print("=" * 80)
    print("ANALISE DE MOMENTUM")
    print("=" * 80)
    
    rsi = momentum['RSI']
    stoch_k = momentum['Stochastic_RSI_K']
    stoch_d = momentum['Stochastic_RSI_D']
    macd = momentum['MACD']
    macd_signal = momentum['MACD_Signal']
    macd_hist = momentum['MACD_Histogram']
    
    print(f"RSI:                {rsi:.2f}")
    if rsi > 70:
        print("                    -> SOBRECOMPRADO (>70)")
    elif rsi < 30:
        print("                    -> SOBREVENDIDO (<30)")
    else:
        print("                    -> NEUTRO (30-70)")
    print()
    
    print(f"Stochastic RSI K:   {stoch_k:.2f}")
    print(f"Stochastic RSI D:   {stoch_d:.2f}")
    if stoch_k > 80:
        print("                    -> SOBRECOMPRADO (>80)")
    elif stoch_k < 20:
        print("                    -> SOBREVENDIDO (<20)")
    else:
        print("                    -> NEUTRO (20-80)")
    print()
    
    print(f"MACD:               {macd:.4f}")
    print(f"MACD Signal:        {macd_signal:.4f}")
    print(f"MACD Histogram:     {macd_hist:.4f}")
    if macd > macd_signal:
        print("                    -> SINAL DE COMPRA (MACD > Signal)")
    else:
        print("                    -> SINAL DE VENDA (MACD < Signal)")
    print()
    
    print("=" * 80)
    print("ANALISE DE VOLATILIDADE")
    print("=" * 80)
    
    atr = volatility['ATR']
    bb_upper = volatility['BB_Upper']
    bb_middle = volatility['BB_Middle']
    bb_lower = volatility['BB_Lower']
    
    print(f"ATR:                ${atr:,.2f}")
    print(f"                    -> Volatilidade {'ALTA' if atr > 1000 else 'MEDIA' if atr > 500 else 'BAIXA'}")
    print()
    
    print(f"Bollinger Superior: ${bb_upper:,.2f}")
    print(f"Bollinger Medio:    ${bb_middle:,.2f}")
    print(f"Bollinger Inferior: ${bb_lower:,.2f}")
    print(f"Preco Atual:        ${current_price:,.2f}")
    
    # Posição nas Bandas de Bollinger
    bb_range = bb_upper - bb_lower
    bb_position = ((current_price - bb_lower) / bb_range) * 100 if bb_range > 0 else 50
    
    print(f"Posicao nas Bandas: {bb_position:.1f}%")
    if bb_position > 80:
        print("                    -> PROXIMO DA BANDA SUPERIOR (Possivel sobrecompra)")
    elif bb_position < 20:
        print("                    -> PROXIMO DA BANDA INFERIOR (Possivel sobrevenda)")
    else:
        print("                    -> NO MEIO DAS BANDAS (Neutro)")
    print()
    
    print("=" * 80)
    print("ANALISE DE VOLUME")
    print("=" * 80)
    
    volume_ma = volume['Volume_MA']
    mfi = volume['MFI']
    obv = volume['OBV']
    current_vol = price['current_volume']
    
    print(f"Volume Atual:       {current_vol:,.2f}")
    print(f"Volume MA(20):      {volume_ma:,.2f}")
    if current_vol > volume_ma:
        print(f"                    -> Volume {((current_vol/volume_ma - 1) * 100):.1f}% acima da media (FORTE)")
    else:
        print(f"                    -> Volume {((1 - current_vol/volume_ma) * 100):.1f}% abaixo da media (FRACO)")
    print()
    
    print(f"MFI:                {mfi:.2f}")
    if mfi > 80:
        print("                    -> SOBRECOMPRADO (>80)")
    elif mfi < 20:
        print("                    -> SOBREVENDIDO (<20)")
    else:
        print("                    -> NEUTRO (20-80)")
    print()
    
    print(f"OBV:                {obv:,.0f}")
    if obv > 0:
        print("                    -> PRESSAO COMPRADORA DOMINANTE")
    else:
        print("                    -> PRESSAO VENDEDORA DOMINANTE")
    print()
    
    print("=" * 80)
    print("ANALISE DE FORCA DA TENDENCIA")
    print("=" * 80)
    
    adx = strength['ADX']
    print(f"ADX:                {adx:.2f}")
    if adx > 25:
        print("                    -> TENDENCIA FORTE (>25)")
    elif adx > 20:
        print("                    -> TENDENCIA MODERADA (20-25)")
    else:
        print("                    -> SEM TENDENCIA DEFINIDA (<20)")
    print()
    
    print("=" * 80)
    print("CONCLUSAO GERAL")
    print("=" * 80)
    
    # Análise geral simplificada
    bullish_signals = 0
    bearish_signals = 0
    
    # Tendência
    if current_price > ema50:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    if ema9 > ema21:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # Momentum
    if rsi > 50:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    if macd > macd_signal:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # Volume
    if mfi > 50:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    if obv > 0:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    total_signals = bullish_signals + bearish_signals
    bullish_percent = (bullish_signals / total_signals) * 100
    bearish_percent = (bearish_signals / total_signals) * 100
    
    print(f"Sinais Altistas:    {bullish_signals}/6 ({bullish_percent:.1f}%)")
    print(f"Sinais Baixistas:   {bearish_signals}/6 ({bearish_percent:.1f}%)")
    print()
    
    if bullish_signals > bearish_signals:
        bias = "ALTISTA"
        strength_level = "FORTE" if bullish_signals >= 5 else "MODERADO"
    elif bearish_signals > bullish_signals:
        bias = "BAIXISTA"
        strength_level = "FORTE" if bearish_signals >= 5 else "MODERADO"
    else:
        bias = "NEUTRO"
        strength_level = "INDEFINIDO"
    
    print(f">>> VIÉS DO MERCADO: {bias} ({strength_level})")
    print()
    
    print("=" * 80)
    print("JSON COMPLETO DOS INDICADORES")
    print("=" * 80)
    print(json.dumps(indicators, indent=2, ensure_ascii=False))
    print()


if __name__ == "__main__":
    # Pode testar com diferentes símbolos
    symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
    
    # Análise do Bitcoin por padrão
    analyze_with_new_indicators("BTC/USDT")
    
    # Descomentar para analisar outros ativos
    # for symbol in symbols:
    #     analyze_with_new_indicators(symbol)
    #     print("\n\n")

