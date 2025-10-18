"""
Testes para o gerador de comentários com IA
"""
import os
from app.utils.ai_analyzer import generate_ai_comment, AIAnalyzer


def test_generate_ai_comment_basic():
    """Testa geração de comentário com dados básicos"""
    
    indicators = {
        'rsi': 55.5,
        'ema9': 42000.50,
        'ema21': 41500.25,
        'ema200': 40000.00,
        'macd': 150.25,
        'macd_signal': 145.50,
        'macd_histogram': 4.75,
        'volume_ma': 25000000,
        'current_volume': 32000000,
        'atr': 800.50,
        'last_close': 42100.00
    }
    
    score = 0.65
    symbol = "Bitcoin"
    
    print("=" * 80)
    print("TEST 1: Bitcoin com Score 0.65 (Tendência Positiva)")
    print("=" * 80)
    
    comment = generate_ai_comment(indicators, score, symbol)
    
    print(f"\n📊 Indicadores:")
    print(f"   RSI: {indicators['rsi']}")
    print(f"   Score: {score}")
    print(f"\n🤖 Comentário gerado:")
    print(f"   {comment}")
    print("\n")
    
    assert isinstance(comment, str)
    assert len(comment) > 50
    assert symbol in comment or "Bitcoin" in comment or "BTC" in comment


def test_generate_ai_comment_bearish():
    """Testa geração de comentário com tendência de baixa"""
    
    indicators = {
        'rsi': 28.5,
        'ema9': 41000.50,
        'ema21': 42500.25,
        'ema200': 43000.00,
        'macd': -120.25,
        'macd_signal': -100.50,
        'macd_histogram': -19.75,
        'volume_ma': 25000000,
        'current_volume': 18000000,
        'atr': 900.50,
        'last_close': 40500.00
    }
    
    score = 0.25
    symbol = "Ethereum"
    
    print("=" * 80)
    print("TEST 2: Ethereum com Score 0.25 (Tendência Negativa)")
    print("=" * 80)
    
    comment = generate_ai_comment(indicators, score, symbol)
    
    print(f"\n📊 Indicadores:")
    print(f"   RSI: {indicators['rsi']} (oversold)")
    print(f"   Score: {score}")
    print(f"\n🤖 Comentário gerado:")
    print(f"   {comment}")
    print("\n")
    
    assert isinstance(comment, str)
    assert len(comment) > 50


def test_generate_ai_comment_neutral():
    """Testa geração de comentário com mercado neutro"""
    
    indicators = {
        'rsi': 50.0,
        'ema9': 100.50,
        'ema21': 100.25,
        'ema200': 99.00,
        'macd': 0.25,
        'macd_signal': 0.20,
        'macd_histogram': 0.05,
        'volume_ma': 1000000,
        'current_volume': 1050000,
        'atr': 2.50,
        'last_close': 100.00
    }
    
    score = 0.50
    symbol = "Solana"
    
    print("=" * 80)
    print("TEST 3: Solana com Score 0.50 (Mercado Neutro)")
    print("=" * 80)
    
    comment = generate_ai_comment(indicators, score, symbol)
    
    print(f"\n📊 Indicadores:")
    print(f"   RSI: {indicators['rsi']} (neutro)")
    print(f"   Score: {score}")
    print(f"\n🤖 Comentário gerado:")
    print(f"   {comment}")
    print("\n")
    
    assert isinstance(comment, str)
    assert len(comment) > 50


def test_fallback_without_api_key():
    """Testa geração de comentário sem API key (fallback)"""
    
    # Salva a API key atual (se existir)
    original_key = os.environ.get('ANTHROPIC_API_KEY')
    
    # Remove temporariamente a API key
    if 'ANTHROPIC_API_KEY' in os.environ:
        del os.environ['ANTHROPIC_API_KEY']
    
    try:
        indicators = {
            'rsi': 65.0,
            'ema9': 42000.50,
            'ema21': 41500.25,
            'current_volume': 30000000,
            'volume_ma': 25000000,
        }
        
        score = 0.70
        symbol = "Bitcoin"
        
        print("=" * 80)
        print("TEST 4: Fallback sem API Key (Análise Baseada em Regras)")
        print("=" * 80)
        
        analyzer = AIAnalyzer()
        comment = analyzer.generate_ai_comment(indicators, score, symbol)
        
        print(f"\n📊 Indicadores:")
        print(f"   RSI: {indicators['rsi']}")
        print(f"   Score: {score}")
        print(f"\n🤖 Comentário gerado (fallback):")
        print(f"   {comment}")
        print("\n")
        
        assert isinstance(comment, str)
        assert len(comment) > 50
        
    finally:
        # Restaura a API key
        if original_key:
            os.environ['ANTHROPIC_API_KEY'] = original_key


def test_with_news():
    """Testa geração de comentário com notícias"""
    
    indicators = {
        'rsi': 60.0,
        'ema9': 42000.50,
        'ema21': 41500.25,
        'current_volume': 35000000,
        'volume_ma': 25000000,
    }
    
    score = 0.68
    symbol = "Bitcoin"
    news = [
        "Bitcoin ETF approval expected this week",
        "Major institution adds BTC to balance sheet",
        "Regulatory clarity improves market sentiment"
    ]
    
    print("=" * 80)
    print("TEST 5: Bitcoin com Notícias")
    print("=" * 80)
    
    comment = generate_ai_comment(indicators, score, symbol, news)
    
    print(f"\n📊 Indicadores:")
    print(f"   RSI: {indicators['rsi']}")
    print(f"   Score: {score}")
    print(f"\n📰 Notícias:")
    for n in news:
        print(f"   - {n}")
    print(f"\n🤖 Comentário gerado:")
    print(f"   {comment}")
    print("\n")
    
    assert isinstance(comment, str)
    assert len(comment) > 50


if __name__ == "__main__":
    print("\n🚀 Iniciando testes do AI Analyzer\n")
    
    try:
        test_generate_ai_comment_basic()
        test_generate_ai_comment_bearish()
        test_generate_ai_comment_neutral()
        test_with_news()
        test_fallback_without_api_key()
        
        print("=" * 80)
        print("✅ Todos os testes passaram!")
        print("=" * 80)
        
    except AssertionError as e:
        print(f"\n❌ Erro no teste: {e}\n")
    except Exception as e:
        print(f"\n⚠️ Erro inesperado: {e}\n")

