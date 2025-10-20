"""
Script para testar atualizacao em tempo real
Executa duas analises consecutivas e compara os resultados
"""
import requests
import time
import json
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def analyze_btc():
    """Faz uma analise do BTC e retorna os dados principais"""
    response = requests.get('http://localhost:8000/analyze/BTC')
    data = response.json()
    return {
        'timestamp': data['last_candle_timestamp'],
        'score': data['score'],
        'rsi': data['indicators']['1d']['momentum']['RSI'],
        'macd': data['indicators']['1d']['momentum']['MACD'],
        'trade_probability': data.get('trade_opportunity', {}).get('probability', 0)
    }

def main():
    print("=" * 70)
    print("TESTE DE ATUALIZACAO EM TEMPO REAL")
    print("=" * 70)
    print()
    
    # Primeira analise
    print(">>> PRIMEIRA ANALISE")
    print("-" * 70)
    analysis1 = analyze_btc()
    print(f"Timestamp do ultimo candle: {analysis1['timestamp']}")
    print(f"Score:                      {analysis1['score']:.4f} ({analysis1['score']*100:.1f}%)")
    print(f"RSI (14):                   {analysis1['rsi']:.2f}")
    print(f"MACD:                       {analysis1['macd']:.2f}")
    print(f"Trade Rapido:               {analysis1['trade_probability']*100:.0f}%")
    print()
    
    # Aguarda alguns segundos
    wait_seconds = 3
    print(f"Aguardando {wait_seconds} segundos antes da segunda analise...")
    time.sleep(wait_seconds)
    print()
    
    # Segunda analise
    print(">>> SEGUNDA ANALISE")
    print("-" * 70)
    analysis2 = analyze_btc()
    print(f"Timestamp do ultimo candle: {analysis2['timestamp']}")
    print(f"Score:                      {analysis2['score']:.4f} ({analysis2['score']*100:.1f}%)")
    print(f"RSI (14):                   {analysis2['rsi']:.2f}")
    print(f"MACD:                       {analysis2['macd']:.2f}")
    print(f"Trade Rapido:               {analysis2['trade_probability']*100:.0f}%")
    print()
    
    # Comparacao
    print("=" * 70)
    print("COMPARACAO DOS RESULTADOS")
    print("=" * 70)
    
    timestamp_changed = analysis1['timestamp'] != analysis2['timestamp']
    score_changed = abs(analysis1['score'] - analysis2['score']) > 0.0001
    rsi_changed = abs(analysis1['rsi'] - analysis2['rsi']) > 0.01
    macd_changed = abs(analysis1['macd'] - analysis2['macd']) > 0.01
    trade_changed = abs(analysis1['trade_probability'] - analysis2['trade_probability']) > 0.01
    
    print(f"Timestamp mudou:      {timestamp_changed}")
    print(f"Score mudou:          {score_changed} (Delta = {abs(analysis2['score'] - analysis1['score']):.4f})")
    print(f"RSI mudou:            {rsi_changed} (Delta = {abs(analysis2['rsi'] - analysis1['rsi']):.2f})")
    print(f"MACD mudou:           {macd_changed} (Delta = {abs(analysis2['macd'] - analysis1['macd']):.2f})")
    print(f"Trade Rapido mudou:   {trade_changed} (Delta = {abs(analysis2['trade_probability'] - analysis1['trade_probability'])*100:.1f}%)")
    print()
    
    # Conclusao
    print("=" * 70)
    print("CONCLUSAO")
    print("=" * 70)
    
    if timestamp_changed:
        print("[OK] Timestamp atualizado - Novo candle foi processado!")
    else:
        print("[INFO] Timestamp inalterado - Ainda estamos no mesmo periodo de tempo")
        print("       (Isso e normal se as analises foram feitas dentro da mesma hora)")
    
    if score_changed or rsi_changed or macd_changed:
        print("[OK] Indicadores foram recalculados - Dados em tempo real confirmado!")
    else:
        print("[INFO] Indicadores identicos - Mercado muito estavel neste momento")
    
    print()
    print("OBSERVACAO:")
    print("  - Se os valores mudaram: [OK] Atualizacao em tempo real funcionando!")
    print("  - Se os valores estao iguais: O mercado esta estavel neste exato momento.")
    print("  - Recomendacao: Teste novamente apos mudanca de hora (ex: 15:59 -> 16:01)")
    print()
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("[ERRO] Backend nao esta rodando!")
        print("       Execute: python run.py")
    except Exception as e:
        print(f"[ERRO] {type(e).__name__} - {str(e)}")

