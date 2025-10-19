"""
Funções auxiliares para as rotas
"""
from fastapi import HTTPException
from app.services.crypto_service import CryptoService


def validate_and_normalize_symbol(symbol: str, crypto_service: CryptoService) -> str:
    """
    Valida e normaliza um símbolo de criptomoeda
    
    Args:
        symbol: Símbolo da moeda (BTC, ETH, SOL)
        crypto_service: Instância do CryptoService
        
    Returns:
        Símbolo normalizado (BTC/USDT, ETH/USDT, etc.)
        
    Raises:
        HTTPException: Se o símbolo for inválido
    """
    if not symbol or len(symbol) > 20:
        raise HTTPException(status_code=400, detail="Símbolo inválido")
    
    try:
        return crypto_service.normalize_symbol(symbol)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao normalizar símbolo: {str(e)}")


def handle_crypto_service_error(e: Exception, symbol: str, operation: str = "buscar dados"):
    """
    Trata erros do CryptoService e lança HTTPException apropriada
    
    Args:
        e: Exceção capturada
        symbol: Símbolo da moeda
        operation: Operação sendo realizada
        
    Raises:
        HTTPException: Com código e mensagem apropriados
    """
    if isinstance(e, ValueError):
        raise HTTPException(status_code=400, detail=str(e))
    
    error_msg = str(e).lower()
    if 'network' in error_msg or 'timeout' in error_msg:
        raise HTTPException(
            status_code=503, 
            detail=f"Erro de conexão com a exchange: {str(e)}"
        )
    elif 'exchange' in error_msg:
        raise HTTPException(
            status_code=400, 
            detail=f"Erro da exchange: {str(e)}"
        )
    else:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao {operation}: {str(e)}"
        )

