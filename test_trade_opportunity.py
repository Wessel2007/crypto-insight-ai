"""
Script de teste para a funcionalidade de análise de trade rápido
"""
import requests
import json

def test_trade_opportunity(symbol: str = "BTC"):
    """
    Testa a análise de oportunidade de trade rápido
    
    Args:
        symbol: Símbolo da criptomoeda (padrão: BTC)
    """
    print(f"🔍 Testando análise de trade rápido para {symbol}...\n")
    
    try:
        # Faz requisição para a API
        url = f"http://localhost:8000/analyze/{symbol}"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"❌ Erro na requisição: Status {response.status_code}")
            print(f"Resposta: {response.text}")
            return
        
        # Parse da resposta
        data = response.json()
        
        # Exibe informações gerais
        print("📊 INFORMAÇÕES GERAIS")
        print("=" * 60)
        print(f"Símbolo: {data['symbol']}")
        print(f"Score Geral: {data['score']}")
        print(f"Diagnóstico: {data['diagnostic']}\n")
        
        # Exibe análise de trade rápido
        if 'trade_opportunity' in data and data['trade_opportunity']:
            trade_opp = data['trade_opportunity']
            print("⚡ ANÁLISE DE TRADE RÁPIDO (Timeframe 1h)")
            print("=" * 60)
            print(f"Probabilidade: {trade_opp['probability']:.0%}")
            print(f"Comentário: {trade_opp['comment']}")
            
            # Exibe indicador visual
            probability = trade_opp['probability']
            if probability >= 0.7:
                print("\n🟢 SINAL FORTE - Alta probabilidade de movimento positivo!")
            elif probability >= 0.4:
                print("\n🟡 SINAL MODERADO - Aguarde confirmação adicional")
            else:
                print("\n🔴 SEM SINAL - Não há oportunidade clara no momento")
        else:
            print("⚠️ Análise de trade rápido não disponível")
        
        print("\n" + "=" * 60)
        
        # Exibe indicadores do timeframe 1h (detalhes técnicos)
        if '1h' in data['indicators']:
            indicators_1h = data['indicators']['1h']
            print("\n📈 INDICADORES TÉCNICOS (1h)")
            print("=" * 60)
            
            # Momentum
            if indicators_1h['momentum']['RSI'] is not None:
                rsi = indicators_1h['momentum']['RSI']
                print(f"RSI: {rsi:.2f}")
                if 40 <= rsi <= 60:
                    print("  ✓ RSI em zona neutra (favorável para entry)")
            
            # Trend
            ema9 = indicators_1h['trend']['EMA9']
            ema21 = indicators_1h['trend']['EMA21']
            if ema9 and ema21:
                print(f"EMA9: {ema9:.2f}")
                print(f"EMA21: {ema21:.2f}")
                if ema9 > ema21:
                    print("  ✓ EMA9 acima de EMA21 (tendência de alta)")
                else:
                    print("  ✗ EMA9 abaixo de EMA21 (tendência de baixa)")
            
            # Volume
            if indicators_1h['volume']['Volume_MA'] is not None:
                volume_ma = indicators_1h['volume']['Volume_MA']
                current_volume = indicators_1h['price']['current_volume']
                if current_volume and current_volume > volume_ma:
                    print(f"Volume: Acima da média")
                    print("  ✓ Volume confirmando movimento")
                else:
                    print(f"Volume: Abaixo da média")
            
            # MACD
            if indicators_1h['momentum']['MACD_Histogram'] is not None:
                macd_hist = indicators_1h['momentum']['MACD_Histogram']
                if macd_hist > 0:
                    print(f"MACD Histograma: {macd_hist:.2f} (positivo)")
                    print("  ✓ MACD em zona positiva")
                else:
                    print(f"MACD Histograma: {macd_hist:.2f} (negativo)")
            
            # ADX
            if indicators_1h['strength']['ADX'] is not None:
                adx = indicators_1h['strength']['ADX']
                print(f"ADX: {adx:.2f}")
                if adx > 25:
                    print("  ✓ Tendência forte (ADX > 25)")
                else:
                    print("  ✗ Tendência fraca (ADX < 25)")
        
        print("\n" + "=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print("Certifique-se de que o servidor está rodando (python run.py)")
    except Exception as e:
        print(f"❌ Erro inesperado: {type(e).__name__} - {str(e)}")


def compare_multiple_cryptos():
    """
    Compara oportunidades de trade rápido entre várias criptomoedas
    """
    symbols = ["BTC", "ETH", "SOL"]
    results = []
    
    print("🔍 Comparando oportunidades de trade rápido...\n")
    
    for symbol in symbols:
        try:
            url = f"http://localhost:8000/analyze/{symbol}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'trade_opportunity' in data and data['trade_opportunity']:
                    results.append({
                        'symbol': symbol,
                        'probability': data['trade_opportunity']['probability'],
                        'comment': data['trade_opportunity']['comment'],
                        'score': data['score']
                    })
        except Exception as e:
            print(f"⚠️ Erro ao analisar {symbol}: {str(e)}")
    
    # Ordena por probabilidade (maior para menor)
    results.sort(key=lambda x: x['probability'], reverse=True)
    
    print("📊 RANKING DE OPORTUNIDADES")
    print("=" * 80)
    print(f"{'Posição':<10}{'Símbolo':<10}{'Probabilidade':<15}{'Score Geral':<15}{'Status':<30}")
    print("-" * 80)
    
    for idx, result in enumerate(results, 1):
        prob_str = f"{result['probability']:.0%}"
        score_str = f"{result['score']:.2f}"
        
        # Emoji baseado na probabilidade
        if result['probability'] >= 0.7:
            emoji = "🟢"
        elif result['probability'] >= 0.4:
            emoji = "🟡"
        else:
            emoji = "🔴"
        
        print(f"{idx:<10}{result['symbol']:<10}{prob_str:<15}{score_str:<15}{emoji} {result['comment']}")
    
    print("=" * 80)


if __name__ == "__main__":
    import sys
    
    print("\n" + "=" * 80)
    print(" 🚀 TESTE DE ANÁLISE DE TRADE RÁPIDO - Cripto Insight")
    print("=" * 80 + "\n")
    
    if len(sys.argv) > 1:
        # Testa símbolo específico se fornecido
        symbol = sys.argv[1]
        test_trade_opportunity(symbol)
    else:
        # Testa BTC por padrão
        test_trade_opportunity("BTC")
        
        # Pergunta se quer comparar múltiplas moedas
        print("\n" + "-" * 80)
        print("\n💡 Quer comparar múltiplas criptomoedas? (BTC, ETH, SOL)")
        response = input("Digite 's' para sim ou Enter para sair: ")
        
        if response.lower() == 's':
            print()
            compare_multiple_cryptos()
    
    print("\n✅ Teste concluído!\n")

