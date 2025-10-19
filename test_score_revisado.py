"""
Teste do novo sistema de score revisado

Este script demonstra o novo cálculo de score com:
- Tendência (EMAs, ADX): 40%
- Momento (RSI, MACD, Stochastic): 30%
- Volume e volatilidade (MFI, ATR, Bollinger): 20%
- Sentimento: 10%

Textos finais:
- >= 0.7 → "Alta probabilidade de alta"
- 0.4–0.69 → "Tendência neutra com leve viés de alta"
- < 0.4 → "Baixa probabilidade de alta / possível queda"
"""

from app.utils.score_engine import ScoreEngine


def print_separator():
    print("\n" + "=" * 80 + "\n")


def test_scenario(title, indicators, last_close, current_volume):
    """Testa um cenário específico"""
    print(f"[TESTE] {title}")
    print(f"Preco: ${last_close:,.2f}")
    print(f"Volume: {current_volume:,.0f}")
    
    # Calcula score
    score = ScoreEngine.calculate_overall_score(indicators, last_close, current_volume)
    diagnostic = ScoreEngine.get_diagnostic(score, indicators)
    
    print(f"\n[SCORE] Score Final: {score:.2f}")
    print(f"[DIAGNOSTICO] {diagnostic}")
    
    # Análise de trade rápido
    trade_analysis = ScoreEngine.analyze_short_term_opportunity(indicators, last_close, current_volume)
    print(f"\n[TRADE RAPIDO]")
    print(f"   Probabilidade: {trade_analysis['probability']:.2f}")
    print(f"   Comentario: {trade_analysis['comment']}")
    
    print_separator()


def main():
    print("=" * 80)
    print("TESTE DO SISTEMA DE SCORE REVISADO")
    print("=" * 80)
    print("\nPesos aplicados:")
    print("  - Tendencia (EMAs, ADX): 40%")
    print("  - Momento (RSI, MACD, Stochastic): 30%")
    print("  - Volume/Volatilidade (MFI, ATR, Bollinger): 20%")
    print("  - Sentimento: 10% (neutro)")
    print_separator()
    
    # ========== CENÁRIO 1: ALTA PROBABILIDADE DE ALTA (>= 0.7) ==========
    print("CENARIO 1: Forte tendencia de alta")
    
    indicators_bullish = {
        'trend': {
            'EMA9': 42500,
            'EMA21': 42000,
            'EMA50': 41500,
            'EMA200': 40000,
            'SMA100': 40500
        },
        'momentum': {
            'RSI': 65,  # Forte mas não sobrecomprado
            'Stochastic_RSI_K': 75,
            'Stochastic_RSI_D': 65,
            'MACD': 150,
            'MACD_Signal': 100,
            'MACD_Histogram': 50  # Positivo
        },
        'volatility': {
            'ATR': 800,  # ~2% do preço
            'BB_Upper': 43500,
            'BB_Middle': 42500,
            'BB_Lower': 41500
        },
        'volume': {
            'Volume_MA': 1000000,
            'MFI': 65,  # Fluxo de dinheiro positivo
            'OBV': 5000000
        },
        'strength': {
            'ADX': 30  # Tendência forte
        }
    }
    
    test_scenario(
        "Cenário Bullish Forte",
        indicators_bullish,
        last_close=42500,
        current_volume=1500000  # Acima da média
    )
    
    # ========== CENÁRIO 2: TENDÊNCIA NEUTRA COM LEVE VIÉS DE ALTA (0.4-0.69) ==========
    print("CENARIO 2: Tendencia neutra com leve vies de alta")
    
    indicators_neutral = {
        'trend': {
            'EMA9': 42100,
            'EMA21': 42050,  # Praticamente cruzadas
            'EMA50': 42000,
            'EMA200': 41500,
            'SMA100': 41800
        },
        'momentum': {
            'RSI': 52,  # Neutro
            'Stochastic_RSI_K': 55,
            'Stochastic_RSI_D': 50,
            'MACD': 20,
            'MACD_Signal': 15,
            'MACD_Histogram': 5  # Levemente positivo
        },
        'volatility': {
            'ATR': 600,
            'BB_Upper': 43000,
            'BB_Middle': 42000,
            'BB_Lower': 41000
        },
        'volume': {
            'Volume_MA': 1000000,
            'MFI': 52,  # Neutro
            'OBV': 3000000
        },
        'strength': {
            'ADX': 18  # Tendência fraca
        }
    }
    
    test_scenario(
        "Cenário Neutro com Leve Viés de Alta",
        indicators_neutral,
        last_close=42000,
        current_volume=950000  # Próximo da média
    )
    
    # ========== CENÁRIO 3: BAIXA PROBABILIDADE DE ALTA / POSSÍVEL QUEDA (< 0.4) ==========
    print("CENARIO 3: Baixa probabilidade de alta / possivel queda")
    
    indicators_bearish = {
        'trend': {
            'EMA9': 41500,
            'EMA21': 42000,  # EMA9 < EMA21 (bearish)
            'EMA50': 42500,
            'EMA200': 43000,  # Preço abaixo de todas
            'SMA100': 42800
        },
        'momentum': {
            'RSI': 35,  # Baixo
            'Stochastic_RSI_K': 25,
            'Stochastic_RSI_D': 30,
            'MACD': -100,
            'MACD_Signal': -80,
            'MACD_Histogram': -20  # Negativo
        },
        'volatility': {
            'ATR': 1000,  # Alta volatilidade
            'BB_Upper': 43000,
            'BB_Middle': 42000,
            'BB_Lower': 41000
        },
        'volume': {
            'Volume_MA': 1000000,
            'MFI': 35,  # Fluxo de dinheiro negativo
            'OBV': 2000000
        },
        'strength': {
            'ADX': 28  # Tendência forte (mas de baixa)
        }
    }
    
    test_scenario(
        "Cenário Bearish",
        indicators_bearish,
        last_close=41500,
        current_volume=1200000  # Volume alto em movimento de baixa
    )
    
    # ========== CENÁRIO 4: TESTE DE FAIXA LIMITE (SCORE PRÓXIMO A 0.7) ==========
    print("CENARIO 4: Teste de faixa limite (proximo a 0.7)")
    
    indicators_limit = {
        'trend': {
            'EMA9': 42300,
            'EMA21': 42100,
            'EMA50': 41900,
            'EMA200': 41000,
            'SMA100': 41500
        },
        'momentum': {
            'RSI': 62,
            'Stochastic_RSI_K': 70,
            'Stochastic_RSI_D': 65,
            'MACD': 100,
            'MACD_Signal': 80,
            'MACD_Histogram': 20
        },
        'volatility': {
            'ATR': 700,
            'BB_Upper': 43000,
            'BB_Middle': 42200,
            'BB_Lower': 41400
        },
        'volume': {
            'Volume_MA': 1000000,
            'MFI': 60,
            'OBV': 4000000
        },
        'strength': {
            'ADX': 26  # Tendência moderada/forte
        }
    }
    
    test_scenario(
        "Cenário Limite (próximo a 0.7)",
        indicators_limit,
        last_close=42200,
        current_volume=1300000
    )
    
    print("\n[OK] Testes concluidos!")
    print("\n[RESUMO] Textos por faixa de score:")
    print("   - >= 0.70: 'Alta probabilidade de alta'")
    print("   - 0.40-0.69: 'Tendencia neutra com leve vies de alta'")
    print("   - < 0.40: 'Baixa probabilidade de alta / possivel queda'")
    print("\n")


if __name__ == "__main__":
    main()

