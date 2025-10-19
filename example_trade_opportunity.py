"""
Exemplo prático de uso da análise de trade rápido
"""
import requests
from datetime import datetime
import time


def get_trade_opportunity(symbol: str) -> dict:
    """
    Obtém a análise de oportunidade de trade para um símbolo
    
    Args:
        symbol: Símbolo da criptomoeda (BTC, ETH, SOL, etc.)
    
    Returns:
        Dicionário com análise completa
    """
    try:
        url = f"http://localhost:8000/analyze/{symbol}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API. Certifique-se de que está rodando.")
        return None
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return None


def should_enter_trade(data: dict) -> tuple[bool, str]:
    """
    Decide se deve entrar em um trade baseado na análise
    
    Args:
        data: Dados retornados pela API
    
    Returns:
        Tupla (deve_entrar, razao)
    """
    if not data or 'trade_opportunity' not in data:
        return False, "Dados insuficientes"
    
    trade_opp = data['trade_opportunity']
    probability = trade_opp['probability']
    score = data['score']
    
    # Regra 1: Probabilidade alta (>= 70%)
    if probability >= 0.7:
        # Verifica se score geral também é favorável (>= 0.6)
        if score >= 0.6:
            return True, f"Sinal forte! Probabilidade {probability:.0%} + Score {score:.2f}"
        else:
            return False, f"Probabilidade alta ({probability:.0%}), mas score geral baixo ({score:.2f})"
    
    # Regra 2: Probabilidade moderada (40-69%)
    elif probability >= 0.4:
        # Só entra se score geral for muito bom (>= 0.7)
        if score >= 0.7:
            return True, f"Sinal moderado com score alto. Prob: {probability:.0%}, Score: {score:.2f}"
        else:
            return False, f"Aguarde confirmação. Prob: {probability:.0%}, Score: {score:.2f}"
    
    # Regra 3: Probabilidade baixa (< 40%)
    else:
        return False, f"Sem oportunidade clara. Probabilidade: {probability:.0%}"


def display_entry_signal(symbol: str, data: dict):
    """
    Exibe sinal de entrada formatado
    
    Args:
        symbol: Símbolo da moeda
        data: Dados da análise
    """
    should_enter, reason = should_enter_trade(data)
    
    print("\n" + "=" * 80)
    print(f"📊 ANÁLISE DE ENTRADA - {symbol}")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Informações principais
    trade_opp = data.get('trade_opportunity', {})
    prob = trade_opp.get('probability', 0)
    comment = trade_opp.get('comment', 'N/A')
    score = data.get('score', 0)
    
    print(f"Probabilidade Trade Rápido: {prob:.0%}")
    print(f"Score Geral: {score:.2f}")
    print(f"Comentário: {comment}\n")
    
    # Decisão
    if should_enter:
        print("🟢 SINAL DE ENTRADA")
        print(f"   {reason}\n")
        
        # Sugestões de operação
        print("💡 SUGESTÕES:")
        if prob >= 0.7:
            print("   • Tipo: Day Trade (2-6 horas)")
            print("   • Objetivo: 2-4% de ganho")
            print("   • Stop Loss: 1-1.5% abaixo da entrada")
        else:
            print("   • Tipo: Swing Trade (1-3 dias)")
            print("   • Objetivo: 4-8% de ganho")
            print("   • Stop Loss: 2-3% abaixo da entrada")
        
        # Indicadores de confirmação
        indicators_1h = data.get('indicators', {}).get('1h', {})
        print("\n✅ CONFIRMAÇÕES:")
        
        if indicators_1h:
            momentum = indicators_1h.get('momentum', {})
            trend = indicators_1h.get('trend', {})
            volume = indicators_1h.get('volume', {})
            
            rsi = momentum.get('RSI')
            if rsi and 40 <= rsi <= 60:
                print(f"   • RSI em zona neutra: {rsi:.1f}")
            
            ema9 = trend.get('EMA9')
            ema21 = trend.get('EMA21')
            if ema9 and ema21 and ema9 > ema21:
                print(f"   • EMA9 > EMA21 (tendência de alta)")
            
            macd_hist = momentum.get('MACD_Histogram')
            if macd_hist and macd_hist > 0:
                print(f"   • MACD positivo: {macd_hist:.2f}")
    
    else:
        print("🔴 NÃO ENTRAR")
        print(f"   {reason}\n")
        
        print("⏳ AGUARDE:")
        print("   • Monitore a cada 1 hora")
        print("   • Entre quando probabilidade > 70%")
        print("   • Confirme com score geral > 0.6")
    
    print("=" * 80 + "\n")


def monitor_multiple_symbols(symbols: list, interval: int = 60):
    """
    Monitora múltiplos símbolos continuamente
    
    Args:
        symbols: Lista de símbolos para monitorar
        interval: Intervalo entre checagens em segundos (padrão: 60s)
    """
    print("🔄 Iniciando monitoramento contínuo...")
    print(f"📋 Símbolos: {', '.join(symbols)}")
    print(f"⏱️ Intervalo: {interval}s\n")
    
    try:
        iteration = 1
        while True:
            print(f"\n{'=' * 80}")
            print(f"🔍 ITERAÇÃO #{iteration} - {datetime.now().strftime('%H:%M:%S')}")
            print(f"{'=' * 80}\n")
            
            opportunities_found = []
            
            for symbol in symbols:
                data = get_trade_opportunity(symbol)
                
                if data:
                    should_enter, reason = should_enter_trade(data)
                    trade_opp = data.get('trade_opportunity', {})
                    prob = trade_opp.get('probability', 0)
                    
                    status = "🟢" if should_enter else "⏸️"
                    print(f"{status} {symbol:6s} | Prob: {prob:>3.0%} | {reason}")
                    
                    if should_enter:
                        opportunities_found.append({
                            'symbol': symbol,
                            'data': data,
                            'reason': reason
                        })
            
            # Exibe detalhes das oportunidades encontradas
            if opportunities_found:
                print(f"\n{'🚀 ' * 20}")
                print("OPORTUNIDADES ENCONTRADAS!")
                print(f"{'🚀 ' * 20}\n")
                
                for opp in opportunities_found:
                    display_entry_signal(opp['symbol'], opp['data'])
            
            # Aguarda próximo ciclo
            print(f"\n⏳ Aguardando {interval}s para próxima checagem...")
            print(f"   (Pressione Ctrl+C para parar)\n")
            
            time.sleep(interval)
            iteration += 1
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Monitoramento interrompido pelo usuário")
        print("✅ Encerrando...\n")


# ============================================================================
# EXEMPLOS DE USO
# ============================================================================

def exemplo_1_consulta_simples():
    """Exemplo 1: Consulta simples de um símbolo"""
    print("\n📌 EXEMPLO 1: Consulta Simples\n")
    
    data = get_trade_opportunity("BTC")
    
    if data:
        display_entry_signal("BTC", data)


def exemplo_2_comparar_multiplos():
    """Exemplo 2: Comparar múltiplas moedas"""
    print("\n📌 EXEMPLO 2: Comparar Múltiplas Moedas\n")
    
    symbols = ["BTC", "ETH", "SOL"]
    results = []
    
    for symbol in symbols:
        data = get_trade_opportunity(symbol)
        if data:
            should_enter, reason = should_enter_trade(data)
            trade_opp = data.get('trade_opportunity', {})
            
            results.append({
                'symbol': symbol,
                'probability': trade_opp.get('probability', 0),
                'score': data.get('score', 0),
                'should_enter': should_enter,
                'reason': reason
            })
    
    # Ordena por probabilidade
    results.sort(key=lambda x: x['probability'], reverse=True)
    
    print("📊 RANKING DE OPORTUNIDADES")
    print("=" * 80)
    print(f"{'#':<4}{'Símbolo':<10}{'Prob':<8}{'Score':<8}{'Entrar?':<10}{'Razão':<40}")
    print("-" * 80)
    
    for idx, r in enumerate(results, 1):
        status = "✅ SIM" if r['should_enter'] else "❌ NÃO"
        print(f"{idx:<4}{r['symbol']:<10}{r['probability']:<7.0%}{r['score']:<8.2f}{status:<10}{r['reason'][:38]}")
    
    print("=" * 80 + "\n")


def exemplo_3_monitoramento():
    """Exemplo 3: Monitoramento contínuo"""
    print("\n📌 EXEMPLO 3: Monitoramento Contínuo\n")
    
    symbols = ["BTC", "ETH", "SOL"]
    monitor_multiple_symbols(symbols, interval=60)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("\n" + "=" * 80)
    print("🚀 CRIPTO INSIGHT - EXEMPLOS DE ANÁLISE DE TRADE RÁPIDO")
    print("=" * 80)
    
    # Menu de opções
    print("\nEscolha um exemplo:\n")
    print("1 - Consulta simples (BTC)")
    print("2 - Comparar múltiplas moedas (BTC, ETH, SOL)")
    print("3 - Monitoramento contínuo (atualiza a cada 1min)")
    print("0 - Sair\n")
    
    choice = input("Digite sua escolha (1-3): ").strip()
    
    if choice == "1":
        exemplo_1_consulta_simples()
    elif choice == "2":
        exemplo_2_comparar_multiplos()
    elif choice == "3":
        exemplo_3_monitoramento()
    elif choice == "0":
        print("\n👋 Até logo!\n")
    else:
        print("\n❌ Opção inválida!\n")
        print("💡 Dica: Execute com argumentos diretos:")
        print("   python example_trade_opportunity.py 1")
        print("   python example_trade_opportunity.py 2")
        print("   python example_trade_opportunity.py 3\n")

