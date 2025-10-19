"""
Crypto Insight AI - Backend
FastAPI application para análise de criptomoedas
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import price, analyze
from app.models.schemas import HealthResponse

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Crypto Insight AI",
    description="API para análise técnica de criptomoedas com indicadores e scoring",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(price.router, tags=["Price"])
app.include_router(analyze.router, tags=["Analysis"])


@app.get("/", response_model=HealthResponse)
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Endpoint de health check para verificar se a API está funcionando
    
    Returns:
        Status da API
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

