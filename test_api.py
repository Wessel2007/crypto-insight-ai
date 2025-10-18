"""
Testes básicos para a API Crypto Insight AI

Para rodar os testes:
1. Instale o pytest: pip install pytest httpx
2. Execute: pytest test_api.py -v

Nota: Os testes que fazem chamadas reais à exchange podem falhar
se não houver conexão com a internet.
"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Testa o endpoint de health check"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_health_endpoint():
    """Testa o endpoint /health"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_price_btc():
    """Testa o endpoint de preços para BTC"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/price/BTC")
        
        # Verifica se a resposta é bem-sucedida
        assert response.status_code == 200
        
        data = response.json()
        
        # Verifica a estrutura da resposta
        assert "symbol" in data
        assert "timeframes" in data
        assert data["symbol"] == "BTC/USDT"
        
        # Verifica se os timeframes estão presentes
        assert "1h" in data["timeframes"]
        assert "4h" in data["timeframes"]
        assert "1d" in data["timeframes"]
        
        # Verifica se há candles em cada timeframe
        for tf in ["1h", "4h", "1d"]:
            assert len(data["timeframes"][tf]) > 0
            
            # Verifica a estrutura do primeiro candle
            candle = data["timeframes"][tf][0]
            assert "timestamp" in candle
            assert "open" in candle
            assert "high" in candle
            assert "low" in candle
            assert "close" in candle
            assert "volume" in candle


@pytest.mark.asyncio
async def test_price_eth():
    """Testa o endpoint de preços para ETH"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/price/ETH")
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "ETH/USDT"


@pytest.mark.asyncio
async def test_price_with_usdt():
    """Testa o endpoint com símbolo já no formato correto"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/price/BTC/USDT")
        # Deve funcionar mesmo com o formato diferente
        # (o símbolo BTC/USDT é válido)


@pytest.mark.asyncio
async def test_analyze_eth():
    """Testa o endpoint de análise para ETH"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/analyze/ETH")
        
        assert response.status_code == 200
        
        data = response.json()
        
        # Verifica a estrutura da resposta
        assert "symbol" in data
        assert "timeframes" in data
        assert "indicators" in data
        assert "score" in data
        assert "diagnostic" in data
        
        # Verifica o símbolo
        assert data["symbol"] == "ETH/USDT"
        
        # Verifica os timeframes
        assert data["timeframes"] == ["1h", "4h", "1d"]
        
        # Verifica o score
        assert 0.0 <= data["score"] <= 1.0
        
        # Verifica que há diagnóstico
        assert len(data["diagnostic"]) > 0
        
        # Verifica os indicadores de cada timeframe
        for tf in ["1h", "4h", "1d"]:
            assert tf in data["indicators"]
            indicators = data["indicators"][tf]
            
            # Verifica que os indicadores estão presentes
            # (podem ser None se não houver dados suficientes)
            assert "rsi" in indicators
            assert "ema9" in indicators
            assert "ema21" in indicators
            assert "ema200" in indicators
            assert "volume_ma" in indicators
            assert "macd" in indicators
            assert "macd_signal" in indicators
            assert "macd_histogram" in indicators


@pytest.mark.asyncio
async def test_analyze_sol():
    """Testa o endpoint de análise para SOL"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/analyze/SOL")
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "SOL/USDT"
        assert 0.0 <= data["score"] <= 1.0


@pytest.mark.asyncio
async def test_invalid_symbol():
    """Testa o endpoint com símbolo inválido"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/price/INVALIDSYMBOL")
        # Deve retornar erro 400
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_analyze_score_range():
    """Testa se o score está sempre no intervalo correto"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        for symbol in ["BTC", "ETH", "SOL"]:
            response = await client.get(f"/analyze/{symbol}")
            if response.status_code == 200:
                data = response.json()
                assert 0.0 <= data["score"] <= 1.0, f"Score fora do intervalo para {symbol}"


# Testes de unidade para funções auxiliares
def test_symbol_normalization():
    """Testa a normalização de símbolos"""
    from app.services.crypto_service import CryptoService
    
    service = CryptoService()
    
    assert service.normalize_symbol("BTC") == "BTC/USDT"
    assert service.normalize_symbol("ETH") == "ETH/USDT"
    assert service.normalize_symbol("SOL") == "SOL/USDT"
    assert service.normalize_symbol("BTC/USDT") == "BTC/USDT"
    assert service.normalize_symbol("btc") == "BTC/USDT"


def test_score_calculation():
    """Testa o cálculo de score"""
    from app.utils.score_engine import ScoreEngine
    
    # Testa RSI score
    assert ScoreEngine.calculate_rsi_score(30) == -0.5  # Oversold
    assert ScoreEngine.calculate_rsi_score(70) == 0.5   # Overbought
    assert ScoreEngine.calculate_rsi_score(50) == 0.0   # Neutro
    
    # Testa diagnóstico
    diagnostic = ScoreEngine.get_diagnostic(0.75, {"rsi": 50})
    assert "altista" in diagnostic.lower()
    
    diagnostic = ScoreEngine.get_diagnostic(0.25, {"rsi": 50})
    assert "baixista" in diagnostic.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

