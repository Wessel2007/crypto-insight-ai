"""
Script para testar a função calculate_score
Execute após iniciar o servidor para ver o score e diagnóstico
"""
import requests
import json
from app.services.indicator_service import IndicatorService
from app.services.crypto_service import CryptoService
from app.utils.score_engine import ScoreEngine


def test_calculate_score_local():
    """Testa a função calculate_score localmente"""
    
    print("\n" + "="*70)
    print("🧪 TESTE LOCAL DA FUNÇÃO calculate_score()")
    print("="*70)
    
    # Inicializa serviços
    crypto_service = CryptoService()
    
    # Símbolos para testar
    symbols = ['BTC', 'ETH', 'SOL']
    
    for symbol in symbols:
        try:
            print(f"\n📊 Analisando {symbol}/USDT...")
            print("-" * 70)
            
            # Busca dados
            normalized_symbol = crypto_service.normalize_symbol(symbol)
            df = crypto_service.get_candles(normalized_symbol, '1d', 200)
            
            # Calcula indicadores
            indicators = IndicatorService.get_indicators(df)
            
            # Calcula score
            score_result = ScoreEngine.calculate_score(indicators)
            
            # Exibe resultados
            print(f"\n📈 INDICADORES:")
            print(f"   RSI: {indicators['rsi']:.2f}" if indicators['rsi'] else "   RSI: N/A")
            print(f"   EMA9: {indicators['ema9']:.2f}" if indicators['ema9'] else "   EMA9: N/A")
            print(f"   EMA21: {indicators['ema21']:.2f}" if indicators['ema21'] else "   EMA21: N/A")
            print(f"   EMA200: {indicators['ema200']:.2f}" if indicators['ema200'] else "   EMA200: N/A")
            print(f"   MACD Hist: {indicators['macd_histogram']:.4f}" if indicators['macd_histogram'] else "   MACD Hist: N/A")
            print(f"   Volume: {indicators['current_volume']:.2f}" if indicators['current_volume'] else "   Volume: N/A")
            print(f"   Volume MA: {indicators['volume_ma']:.2f}" if indicators['volume_ma'] else "   Volume MA: N/A")
            print(f"   ATR: {indicators['atr']:.2f}" if indicators['atr'] else "   ATR: N/A")
            
            print(f"\n🎯 SCORE:")
            print(f"   Score Bruto: {score_result['raw_score']}/5")
            print(f"   Score Normalizado: {score_result['normalized_score']:.2f} (-1 a +1)")
            
            print(f"\n💡 DIAGNÓSTICO:")
            print(f"   {score_result['diagnostic']}")
            
            print(f"\n📋 SINAIS DETECTADOS:")
            if score_result['signals']:
                for signal in score_result['signals']:
                    print(f"   {signal}")
            else:
                print("   Nenhum sinal forte detectado")
            
            print(f"\n🔍 BREAKDOWN:")
            for key, value in score_result['score_breakdown'].items():
                status = "✅" if value == "analyzed" else "⚠️"
                print(f"   {status} {key}: {value}")
            
        except Exception as e:
            print(f"❌ Erro ao processar {symbol}: {str(e)}")
    
    print("\n" + "="*70)


def test_calculate_score_via_api():
    """Testa via API (se o endpoint estiver implementado)"""
    
    print("\n" + "="*70)
    print("🌐 TESTE VIA API")
    print("="*70)
    
    BASE_URL = "http://localhost:8000"
    
    symbols = ['BTC', 'ETH', 'SOL']
    
    for symbol in symbols:
        try:
            response = requests.get(f"{BASE_URL}/analyze/{symbol}")
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"\n📊 {data['symbol']}")
                print(f"   Score Geral: {data['score']:.2f}")
                print(f"   Diagnóstico: {data['diagnostic']}")
                
                # Se tiver o novo formato de score detalhado
                if 'detailed_score' in data:
                    print(f"   Score Bruto: {data['detailed_score']['raw_score']}/5")
                    print(f"   Sinais: {len(data['detailed_score']['signals'])}")
            else:
                print(f"❌ Erro {response.status_code} para {symbol}")
                
        except requests.exceptions.ConnectionError:
            print("⚠️ Servidor não está rodando. Use 'python run.py'")
            break
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
    
    print("\n" + "="*70)


def test_score_scenarios():
    """Testa diferentes cenários de score"""
    
    print("\n" + "="*70)
    print("🧪 TESTE DE CENÁRIOS")
    print("="*70)
    
    scenarios = [
        {
            'name': 'Cenário Altista Forte',
            'indicators': {
                'rsi': 25,  # Oversold
                'ema9': 50000,
                'ema21': 49000,  # EMA9 > EMA21
                'ema200': 45000,  # EMA21 > EMA200
                'macd_histogram': 100,  # Positivo
                'current_volume': 1500,
                'volume_ma': 1000,  # Volume alto
                'atr': 500,
                'last_close': 50000
            }
        },
        {
            'name': 'Cenário Baixista Forte',
            'indicators': {
                'rsi': 75,  # Overbought
                'ema9': 48000,
                'ema21': 49000,  # EMA9 < EMA21
                'ema200': 50000,  # Tendência de baixa
                'macd_histogram': -50,  # Negativo
                'current_volume': 800,
                'volume_ma': 1000,  # Volume baixo
                'atr': 12000,
                'last_close': 48000  # ATR > 20%
            }
        },
        {
            'name': 'Cenário Neutro',
            'indicators': {
                'rsi': 50,  # Neutro
                'ema9': 50000,
                'ema21': 49800,  # Levemente acima
                'ema200': 48000,
                'macd_histogram': 10,
                'current_volume': 950,
                'volume_ma': 1000,
                'atr': 800,
                'last_close': 50000
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{'='*70}")
        print(f"📋 {scenario['name']}")
        print('='*70)
        
        indicators = scenario['indicators']
        score_result = ScoreEngine.calculate_score(indicators)
        
        print(f"\n🎯 RESULTADO:")
        print(f"   Score Bruto: {score_result['raw_score']}/5")
        print(f"   Score Normalizado: {score_result['normalized_score']:.2f}")
        print(f"   Diagnóstico: {score_result['diagnostic']}")
        
        print(f"\n📋 SINAIS:")
        for signal in score_result['signals']:
            print(f"   {signal}")
    
    print("\n" + "="*70)


def show_scoring_rules():
    """Mostra as regras de pontuação"""
    
    print("\n" + "="*70)
    print("📚 REGRAS DE PONTUAÇÃO")
    print("="*70)
    
    rules = [
        ("RSI < 30", "+1", "Zona de sobrevenda (oportunidade)"),
        ("RSI > 70", "-1", "Zona de sobrecompra (cautela)"),
        ("EMA9 > EMA21", "+1", "Tendência de alta"),
        ("EMA9 < EMA21", "-1", "Tendência de baixa"),
        ("EMA21 > EMA200", "+1", "Tendência de longo prazo positiva"),
        ("MACD Histogram > 0", "+1", "Momentum positivo"),
        ("Volume > Volume MA", "+1", "Movimento confirmado"),
        ("ATR > 20% do preço", "-1", "Alta volatilidade (risco)")
    ]
    
    print("\n📊 REGRAS:")
    for condition, points, description in rules:
        print(f"\n   {points:>3} ponto(s) - {condition}")
        print(f"        → {description}")
    
    print("\n" + "="*70)
    print("🎯 INTERPRETAÇÃO DO SCORE NORMALIZADO (-1 a +1):")
    print("="*70)
    
    interpretations = [
        ("≥ 0.60", "🟢 Bom momento de compra"),
        ("0.20 a 0.59", "🟡 Neutro de alta"),
        ("-0.20 a 0.19", "⚪ Neutro"),
        ("-0.60 a -0.21", "🟠 Leve tendência de baixa"),
        ("≤ -0.60", "🔴 Evite compra agora")
    ]
    
    for range_val, diagnostic in interpretations:
        print(f"\n   {range_val:>15} → {diagnostic}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    print("\n🚀 TESTE DA FUNÇÃO calculate_score()")
    print("="*70)
    
    try:
        # Mostra as regras
        show_scoring_rules()
        
        # Testa cenários simulados
        test_score_scenarios()
        
        # Testa com dados reais
        print("\n\n💡 TESTANDO COM DADOS REAIS...")
        test_calculate_score_local()
        
        # Testa via API (opcional)
        print("\n\n🌐 Tentando testar via API...")
        test_calculate_score_via_api()
        
        print("\n✅ Testes concluídos!\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido pelo usuário.\n")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {str(e)}\n")

