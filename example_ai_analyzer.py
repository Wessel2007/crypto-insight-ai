"""
Exemplo de uso do AI Analyzer para gerar comentários naturais
"""
from app.utils.ai_analyzer import generate_ai_comment, AIAnalyzer


def exemplo_bitcoin_alta():
    """Exemplo: Bitcoin em tendência de alta"""
    
    print("=" * 80)
    print("📊 EXEMPLO 1: Bitcoin em Tendência de Alta")
    print("=" * 80)
    
    indicators = {
        'rsi': 65.5,
        'ema9': 42500.00,
        'ema21': 41200.00,
        'ema200': 38000.00,
        'macd': 250.50,
        'macd_signal': 220.30,
        'macd_histogram': 30.20,
        'volume_ma': 25000000,
        'current_volume': 35000000,
        'atr': 850.25,
        'last_close': 42300.00
    }
    
    score = 0.75  # 75% - tendência positiva forte
    
    print(f"\n💰 Preço Atual: ${indicators['last_close']:,.2f}")
    print(f"📈 Score: {score:.2f} (75% - Alta Confiança)")
    print(f"📊 RSI: {indicators['rsi']:.1f} (Zona de sobrecompra leve)")
    print(f"📉 EMA9 > EMA21: ✅ (Tendência de alta)")
    print(f"📊 Volume: +40% acima da média")
    
    print(f"\n🤖 Gerando comentário com IA...")
    comment = generate_ai_comment(indicators, score, "Bitcoin")
    
    print(f"\n💬 Comentário gerado:")
    print(f"   \"{comment}\"")
    print("\n")


def exemplo_ethereum_baixa():
    """Exemplo: Ethereum em pressão vendedora"""
    
    print("=" * 80)
    print("📊 EXEMPLO 2: Ethereum com Pressão Vendedora")
    print("=" * 80)
    
    indicators = {
        'rsi': 32.5,
        'ema9': 2100.00,
        'ema21': 2250.00,
        'ema200': 2400.00,
        'macd': -50.25,
        'macd_signal': -35.50,
        'macd_histogram': -14.75,
        'volume_ma': 15000000,
        'current_volume': 22000000,
        'atr': 85.50,
        'last_close': 2050.00
    }
    
    score = 0.30  # 30% - tendência negativa
    
    print(f"\n💰 Preço Atual: ${indicators['last_close']:,.2f}")
    print(f"📉 Score: {score:.2f} (30% - Baixa Confiança)")
    print(f"📊 RSI: {indicators['rsi']:.1f} (Zona de sobrevenda)")
    print(f"📈 EMA9 < EMA21: ❌ (Tendência de baixa)")
    print(f"📊 Volume: +47% acima da média (confirmação de queda)")
    
    print(f"\n🤖 Gerando comentário com IA...")
    comment = generate_ai_comment(indicators, score, "Ethereum")
    
    print(f"\n💬 Comentário gerado:")
    print(f"   \"{comment}\"")
    print("\n")


def exemplo_solana_neutro():
    """Exemplo: Solana em mercado lateral"""
    
    print("=" * 80)
    print("📊 EXEMPLO 3: Solana em Mercado Lateral")
    print("=" * 80)
    
    indicators = {
        'rsi': 48.5,
        'ema9': 95.50,
        'ema21': 95.20,
        'ema200': 94.00,
        'macd': 0.15,
        'macd_signal': 0.12,
        'macd_histogram': 0.03,
        'volume_ma': 8000000,
        'current_volume': 7500000,
        'atr': 3.20,
        'last_close': 95.30
    }
    
    score = 0.52  # 52% - neutro com leve viés de alta
    
    print(f"\n💰 Preço Atual: ${indicators['last_close']:,.2f}")
    print(f"⚖️  Score: {score:.2f} (52% - Neutro)")
    print(f"📊 RSI: {indicators['rsi']:.1f} (Neutro)")
    print(f"📊 EMAs próximas (consolidação)")
    print(f"📊 Volume: -6% abaixo da média")
    
    print(f"\n🤖 Gerando comentário com IA...")
    comment = generate_ai_comment(indicators, score, "Solana")
    
    print(f"\n💬 Comentário gerado:")
    print(f"   \"{comment}\"")
    print("\n")


def exemplo_com_noticias():
    """Exemplo: Bitcoin com notícias positivas"""
    
    print("=" * 80)
    print("📊 EXEMPLO 4: Bitcoin com Notícias Positivas")
    print("=" * 80)
    
    indicators = {
        'rsi': 58.0,
        'ema9': 43000.00,
        'ema21': 42000.00,
        'ema200': 40000.00,
        'macd': 180.25,
        'macd_signal': 165.50,
        'macd_histogram': 14.75,
        'volume_ma': 30000000,
        'current_volume': 45000000,
        'atr': 920.50,
        'last_close': 42800.00
    }
    
    score = 0.72
    
    news = [
        "Bitcoin ETF approval expected this week by SEC",
        "MicroStrategy purchases additional 5,000 BTC",
        "Major bank announces Bitcoin custody services",
        "Institutional demand reaches all-time high"
    ]
    
    print(f"\n💰 Preço Atual: ${indicators['last_close']:,.2f}")
    print(f"📈 Score: {score:.2f} (72% - Alta Confiança)")
    print(f"📊 RSI: {indicators['rsi']:.1f}")
    print(f"📊 Volume: +50% acima da média")
    
    print(f"\n📰 Notícias recentes:")
    for i, n in enumerate(news, 1):
        print(f"   {i}. {n}")
    
    print(f"\n🤖 Gerando comentário com IA (considerando notícias)...")
    comment = generate_ai_comment(indicators, score, "Bitcoin", news)
    
    print(f"\n💬 Comentário gerado:")
    print(f"   \"{comment}\"")
    print("\n")


def exemplo_fallback():
    """Exemplo: Análise sem API key (fallback)"""
    
    print("=" * 80)
    print("📊 EXEMPLO 5: Análise Fallback (Sem API Key)")
    print("=" * 80)
    
    import os
    
    # Remove temporariamente a API key
    original_key = os.environ.get('ANTHROPIC_API_KEY')
    if 'ANTHROPIC_API_KEY' in os.environ:
        del os.environ['ANTHROPIC_API_KEY']
    
    try:
        indicators = {
            'rsi': 70.5,
            'ema9': 44000.00,
            'ema21': 43000.00,
            'current_volume': 40000000,
            'volume_ma': 25000000,
        }
        
        score = 0.68
        
        print(f"\n⚠️  API Key não configurada - usando análise baseada em regras")
        print(f"\n💰 Score: {score:.2f}")
        print(f"📊 RSI: {indicators['rsi']:.1f} (Sobrecompra)")
        print(f"📊 Volume: +60% acima da média")
        
        print(f"\n🤖 Gerando comentário (fallback)...")
        analyzer = AIAnalyzer()
        comment = analyzer.generate_ai_comment(indicators, score, "Bitcoin")
        
        print(f"\n💬 Comentário gerado:")
        print(f"   \"{comment}\"")
        print("\n")
        
    finally:
        # Restaura a API key
        if original_key:
            os.environ['ANTHROPIC_API_KEY'] = original_key


if __name__ == "__main__":
    print("\n")
    print("🚀 " + "EXEMPLOS DE USO DO AI ANALYZER".center(78) + " 🚀")
    print("\n")
    
    try:
        exemplo_bitcoin_alta()
        exemplo_ethereum_baixa()
        exemplo_solana_neutro()
        exemplo_com_noticias()
        exemplo_fallback()
        
        print("=" * 80)
        print("✅ Todos os exemplos executados com sucesso!")
        print("=" * 80)
        print("\n💡 Dica: Configure ANTHROPIC_API_KEY para usar análise com IA")
        print("   Sem API key, o sistema usa análise baseada em regras (fallback)\n")
        
    except Exception as e:
        print(f"\n❌ Erro ao executar exemplos: {e}\n")

