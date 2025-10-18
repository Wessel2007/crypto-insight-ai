"""
Script para testar a função get_indicators
Execute após iniciar o servidor para testar os novos indicadores
"""
import requests
import json


def test_get_indicators():
    """Testa a função get_indicators através da API"""
    
    BASE_URL = "http://localhost:8000"
    
    print("🔬 Testando a função get_indicators com novos indicadores\n")
    print("="*70)
    
    # Testa com ETH
    symbol = "ETH"
    print(f"\n📊 Analisando {symbol}...")
    
    response = requests.get(f"{BASE_URL}/analyze/{symbol}")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\n✅ Análise de {data['symbol']}")
        print(f"Score: {data['score']}")
        print(f"Diagnóstico: {data['diagnostic']}")
        
        print("\n📈 INDICADORES POR TIMEFRAME:")
        
        for timeframe in ['1h', '4h', '1d']:
            ind = data['indicators'][timeframe]
            
            print(f"\n⏰ {timeframe.upper()}:")
            print(f"   RSI (14):          {ind['rsi']:.2f}" if ind['rsi'] else "   RSI (14):          N/A")
            print(f"   EMA 9:             {ind['ema9']:.2f}" if ind['ema9'] else "   EMA 9:             N/A")
            print(f"   EMA 21:            {ind['ema21']:.2f}" if ind['ema21'] else "   EMA 21:            N/A")
            print(f"   EMA 200:           {ind['ema200']:.2f}" if ind['ema200'] else "   EMA 200:           N/A")
            print(f"   MACD:              {ind['macd']:.4f}" if ind['macd'] else "   MACD:              N/A")
            print(f"   MACD Signal:       {ind['macd_signal']:.4f}" if ind['macd_signal'] else "   MACD Signal:       N/A")
            print(f"   MACD Histogram:    {ind['macd_histogram']:.4f}" if ind['macd_histogram'] else "   MACD Histogram:    N/A")
            print(f"   Volume MA (20):    {ind['volume_ma']:.2f}" if ind['volume_ma'] else "   Volume MA (20):    N/A")
            print(f"   ATR (14):          {ind['atr']:.2f} 🆕" if ind['atr'] else "   ATR (14):          N/A 🆕")
        
        print("\n" + "="*70)
        print("\n✨ NOVO INDICADOR ATR (Average True Range) adicionado!")
        print("📊 O ATR mede a volatilidade do mercado")
        print("   • ATR alto = alta volatilidade (movimentos grandes)")
        print("   • ATR baixo = baixa volatilidade (movimentos pequenos)")
        
        print("\n" + "="*70)
        
        # Mostra JSON formatado
        print("\n📄 Resposta JSON completa (1h):\n")
        print(json.dumps(data['indicators']['1h'], indent=2, ensure_ascii=False))
        
        print("\n✅ Teste concluído com sucesso!")
        
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.text)


def test_multiple_symbols():
    """Testa múltiplos símbolos"""
    
    BASE_URL = "http://localhost:8000"
    symbols = ['BTC', 'ETH', 'SOL']
    
    print("\n" + "="*70)
    print("📊 Testando múltiplas criptomoedas\n")
    
    for symbol in symbols:
        response = requests.get(f"{BASE_URL}/analyze/{symbol}")
        
        if response.status_code == 200:
            data = response.json()
            ind_1d = data['indicators']['1d']
            
            print(f"\n{symbol}/USDT:")
            print(f"  Score: {data['score']:.2f}")
            print(f"  RSI: {ind_1d['rsi']:.2f}" if ind_1d['rsi'] else "  RSI: N/A")
            print(f"  ATR: {ind_1d['atr']:.2f} 🆕" if ind_1d['atr'] else "  ATR: N/A 🆕")
            print(f"  Diagnóstico: {data['diagnostic']}")
        else:
            print(f"\n❌ Erro ao buscar {symbol}: {response.status_code}")
    
    print("\n" + "="*70)


def show_indicator_info():
    """Mostra informações sobre os indicadores"""
    
    print("\n" + "="*70)
    print("📚 INDICADORES DISPONÍVEIS NA API")
    print("="*70)
    
    indicators_info = [
        {
            'name': 'RSI (14)',
            'description': 'Relative Strength Index - mede força da tendência',
            'range': '0-100 (< 30 = oversold, > 70 = overbought)',
            'format': '2 casas decimais'
        },
        {
            'name': 'EMA 9, 21, 200',
            'description': 'Exponential Moving Average - médias móveis',
            'range': 'Valor em USD',
            'format': '2 casas decimais'
        },
        {
            'name': 'MACD',
            'description': 'Moving Average Convergence Divergence',
            'range': 'Positivo/Negativo',
            'format': '4 casas decimais'
        },
        {
            'name': 'MACD Signal',
            'description': 'Linha de sinal do MACD',
            'range': 'Positivo/Negativo',
            'format': '4 casas decimais'
        },
        {
            'name': 'MACD Histogram',
            'description': 'Diferença entre MACD e Signal',
            'range': 'Positivo/Negativo',
            'format': '4 casas decimais'
        },
        {
            'name': 'Volume MA (20)',
            'description': 'Média móvel do volume (últimos 20 candles)',
            'range': 'Valor absoluto',
            'format': '2 casas decimais'
        },
        {
            'name': 'ATR (14) 🆕',
            'description': 'Average True Range - mede volatilidade',
            'range': 'Valor em USD (quanto maior, mais volátil)',
            'format': '2 casas decimais'
        }
    ]
    
    for ind in indicators_info:
        print(f"\n📊 {ind['name']}")
        print(f"   Descrição: {ind['description']}")
        print(f"   Range: {ind['range']}")
        print(f"   Formato: {ind['format']}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    print("\n🚀 Teste da função get_indicators")
    print("Certifique-se de que o servidor está rodando em http://localhost:8000\n")
    
    try:
        # Mostra informações sobre os indicadores
        show_indicator_info()
        
        # Testa a função principal
        test_get_indicators()
        
        # Testa múltiplos símbolos
        test_multiple_symbols()
        
        print("\n✅ Todos os testes concluídos!\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar ao servidor.")
        print("Certifique-se de que o servidor está rodando:")
        print("   python run.py\n")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}\n")

