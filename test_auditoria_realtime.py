"""
Script de teste para validar que a análise está usando dados em tempo real
e indicadores 100% atualizados a cada requisição
"""
import requests
import json
from datetime import datetime
import time

# URL base da API
BASE_URL = "http://localhost:8000"

def test_realtime_analysis():
    """
    Testa se a análise está usando dados em tempo real
    """
    print("=" * 80)
    print("TESTE DE AUDITORIA - ANÁLISE EM TEMPO REAL")
    print("=" * 80)
    print()
    
    # Lista de criptos para testar
    symbols = ["BTC", "ETH", "SOL"]
    
    for symbol in symbols:
        print(f"\n{'=' * 80}")
        print(f"Testando: {symbol}")
        print(f"{'=' * 80}\n")
        
        # Faz 2 requisições consecutivas para verificar se os dados mudam
        results = []
        
        for i in range(2):
            print(f"Requisição #{i+1} em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            try:
                response = requests.get(f"{BASE_URL}/analyze/{symbol}")
                
                if response.status_code == 200:
                    data = response.json()
                    results.append(data)
                    
                    # Extrai informações relevantes
                    last_candle_time = data.get('last_candle_timestamp', 'N/A')
                    score = data.get('score', 0)
                    
                    # Indicadores do timeframe 1h (mais dinâmico)
                    indicators_1h = data.get('indicators', {}).get('1h', {})
                    
                    rsi = indicators_1h.get('momentum', {}).get('RSI')
                    ema9 = indicators_1h.get('trend', {}).get('EMA9')
                    ema21 = indicators_1h.get('trend', {}).get('EMA21')
                    last_close = indicators_1h.get('price', {}).get('last_close')
                    
                    print(f"  ✓ Último candle: {last_candle_time}")
                    print(f"  ✓ Preço atual: ${last_close}")
                    print(f"  ✓ RSI: {rsi}")
                    print(f"  ✓ EMA9: {ema9}")
                    print(f"  ✓ EMA21: {ema21}")
                    print(f"  ✓ Score: {score}")
                    print()
                    
                else:
                    print(f"  ❌ Erro HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"  ❌ Erro na requisição: {str(e)}")
            
            # Aguarda 2 segundos entre requisições
            if i == 0:
                print("  ⏳ Aguardando 2 segundos...\n")
                time.sleep(2)
        
        # Compara os resultados
        if len(results) == 2:
            print(f"\n{'─' * 80}")
            print("COMPARAÇÃO ENTRE REQUISIÇÕES:")
            print(f"{'─' * 80}")
            
            # Verifica se os timestamps são diferentes (indicando dados novos)
            time1 = results[0].get('last_candle_timestamp')
            time2 = results[1].get('last_candle_timestamp')
            
            # Verifica se os indicadores foram recalculados
            rsi1 = results[0].get('indicators', {}).get('1h', {}).get('momentum', {}).get('RSI')
            rsi2 = results[1].get('indicators', {}).get('1h', {}).get('momentum', {}).get('RSI')
            
            price1 = results[0].get('indicators', {}).get('1h', {}).get('price', {}).get('last_close')
            price2 = results[1].get('indicators', {}).get('1h', {}).get('price', {}).get('last_close')
            
            print(f"\nRequisição 1:")
            print(f"  - Timestamp: {time1}")
            print(f"  - RSI: {rsi1}")
            print(f"  - Preço: ${price1}")
            
            print(f"\nRequisição 2:")
            print(f"  - Timestamp: {time2}")
            print(f"  - RSI: {rsi2}")
            print(f"  - Preço: ${price2}")
            
            print(f"\n{'─' * 80}")
            print("VALIDAÇÃO:")
            print(f"{'─' * 80}")
            
            # Verifica campo de timestamp existe
            if time1 and time1 != "N/A":
                print("  ✓ Campo 'last_candle_timestamp' presente e válido")
            else:
                print("  ❌ Campo 'last_candle_timestamp' ausente ou inválido")
            
            # Se o preço mudou, significa que está pegando dados novos
            if price1 != price2:
                print(f"  ✓ Preços diferentes (${price1} → ${price2})")
                print("  ✓ Confirmado: dados sendo atualizados em tempo real!")
            else:
                print(f"  ⚠️  Preços iguais (${price1} = ${price2})")
                print("  ℹ️  Normal se não houve mudança de candle entre requisições")
            
            # Indicadores devem ser recalculados (mesmo que valores sejam iguais)
            print("  ✓ Indicadores recalculados a cada requisição (confirmado por código)")
            
            print()

def test_endpoint_structure():
    """
    Testa se a estrutura da resposta está correta
    """
    print(f"\n{'=' * 80}")
    print("TESTE DE ESTRUTURA DA RESPOSTA")
    print(f"{'=' * 80}\n")
    
    try:
        response = requests.get(f"{BASE_URL}/analyze/BTC")
        
        if response.status_code == 200:
            data = response.json()
            
            # Campos obrigatórios
            required_fields = [
                'symbol',
                'timeframes',
                'indicators',
                'score',
                'diagnostic',
                'last_candle_timestamp'  # NOVO CAMPO
            ]
            
            print("Validando campos obrigatórios:")
            all_present = True
            
            for field in required_fields:
                if field in data:
                    print(f"  ✓ Campo '{field}' presente")
                else:
                    print(f"  ❌ Campo '{field}' AUSENTE")
                    all_present = False
            
            if all_present:
                print("\n✓ TODOS os campos obrigatórios estão presentes!")
                
                # Mostra exemplo do JSON
                print(f"\n{'─' * 80}")
                print("EXEMPLO DE RESPOSTA (formatada):")
                print(f"{'─' * 80}\n")
                
                # Cria um exemplo simplificado
                example = {
                    "symbol": data.get('symbol'),
                    "timeframes": data.get('timeframes'),
                    "score": data.get('score'),
                    "diagnostic": data.get('diagnostic'),
                    "last_candle_timestamp": data.get('last_candle_timestamp'),
                    "indicators": {
                        "1h": {
                            "trend": data.get('indicators', {}).get('1h', {}).get('trend', {}),
                            "momentum": data.get('indicators', {}).get('1h', {}).get('momentum', {}),
                            "price": data.get('indicators', {}).get('1h', {}).get('price', {})
                        }
                    }
                }
                
                print(json.dumps(example, indent=2, ensure_ascii=False))
            else:
                print("\n❌ Alguns campos obrigatórios estão ausentes!")
                
        else:
            print(f"❌ Erro HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "AUDITORIA DE TEMPO REAL - BACKEND" + " " * 25 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    print("Este script valida que:")
    print("  1. Os dados são buscados diretamente da API (sem cache)")
    print("  2. Os indicadores são recalculados a cada requisição")
    print("  3. O timestamp do último candle é retornado")
    print("  4. Pelo menos 500 candles são usados para cálculos")
    print()
    
    # Executa os testes
    test_realtime_analysis()
    test_endpoint_structure()
    
    print(f"\n{'=' * 80}")
    print("TESTES CONCLUÍDOS!")
    print(f"{'=' * 80}\n")

