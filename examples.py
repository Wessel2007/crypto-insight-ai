"""
Exemplos de uso da API Crypto Insight AI
Execute este script após iniciar o servidor para testar os endpoints
"""
import requests
import json


BASE_URL = "http://localhost:8000"


def print_response(title: str, response):
    """Imprime a resposta de forma formatada"""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print('='*60)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("\nResposta:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Erro: {response.text}")
    print('='*60)


def test_health_check():
    """Testa o endpoint de health check"""
    response = requests.get(f"{BASE_URL}/")
    print_response("Health Check", response)


def test_price_btc():
    """Testa o endpoint de preços para BTC"""
    response = requests.get(f"{BASE_URL}/price/BTC")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n{'='*60}")
        print(f"📊 Preços do {data['symbol']}")
        print('='*60)
        
        for tf, candles in data['timeframes'].items():
            last_candle = candles[-1]
            print(f"\n⏰ Timeframe: {tf}")
            print(f"   Close: ${last_candle['close']:,.2f}")
            print(f"   High: ${last_candle['high']:,.2f}")
            print(f"   Low: ${last_candle['low']:,.2f}")
            print(f"   Volume: {last_candle['volume']:,.2f}")
        print('='*60)
    else:
        print_response("Erro ao buscar preços", response)


def test_analyze_eth():
    """Testa o endpoint de análise para ETH"""
    response = requests.get(f"{BASE_URL}/analyze/ETH")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n{'='*60}")
        print(f"📈 Análise Técnica: {data['symbol']}")
        print('='*60)
        
        print(f"\n🎯 Score Geral: {data['score']}")
        print(f"📝 Diagnóstico: {data['diagnostic']}")
        
        print("\n📊 Indicadores por Timeframe:")
        for tf in data['timeframes']:
            indicators = data['indicators'][tf]
            print(f"\n⏰ {tf}:")
            print(f"   RSI: {indicators['rsi']:.2f}" if indicators['rsi'] else "   RSI: N/A")
            print(f"   EMA9: {indicators['ema9']:.2f}" if indicators['ema9'] else "   EMA9: N/A")
            print(f"   EMA21: {indicators['ema21']:.2f}" if indicators['ema21'] else "   EMA21: N/A")
            print(f"   EMA200: {indicators['ema200']:.2f}" if indicators['ema200'] else "   EMA200: N/A")
            print(f"   MACD: {indicators['macd']:.4f}" if indicators['macd'] else "   MACD: N/A")
            print(f"   MACD Signal: {indicators['macd_signal']:.4f}" if indicators['macd_signal'] else "   MACD Signal: N/A")
        
        print('='*60)
    else:
        print_response("Erro ao analisar", response)


def test_analyze_sol():
    """Testa o endpoint de análise para SOL"""
    response = requests.get(f"{BASE_URL}/analyze/SOL")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n{'='*60}")
        print(f"📈 Análise Técnica: {data['symbol']}")
        print('='*60)
        print(f"\n🎯 Score: {data['score']}")
        print(f"📝 {data['diagnostic']}")
        print('='*60)
    else:
        print_response("Erro ao analisar SOL", response)


def run_all_tests():
    """Executa todos os testes"""
    print("\n🚀 Testando Crypto Insight AI API")
    print("Certifique-se de que o servidor está rodando em http://localhost:8000\n")
    
    try:
        # Test 1: Health Check
        test_health_check()
        
        # Test 2: Preços do Bitcoin
        test_price_btc()
        
        # Test 3: Análise do Ethereum
        test_analyze_eth()
        
        # Test 4: Análise do Solana
        test_analyze_sol()
        
        print("\n✅ Todos os testes concluídos!\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar ao servidor.")
        print("Certifique-se de que o servidor está rodando:")
        print("   python run.py")
        print("\nou")
        print("   uvicorn app.main:app --reload\n")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}\n")


if __name__ == "__main__":
    run_all_tests()

