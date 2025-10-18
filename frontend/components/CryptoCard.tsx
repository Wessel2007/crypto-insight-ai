import React, { useState } from 'react';
import { TrendingUp, TrendingDown, AlertCircle, Activity, BarChart3 } from 'lucide-react';
import { analyzeCrypto, AnalysisResponse } from '@/lib/api';

interface CryptoCardProps {
  symbol: string;
  name: string;
  icon: string;
}

const CryptoCard: React.FC<CryptoCardProps> = ({ symbol, name, icon }) => {
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await analyzeCrypto(symbol);
      setAnalysis(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
      setAnalysis(null);
    } finally {
      setLoading(false);
    }
  };

  // Converte score de 0-1 para 0-100 para exibição
  const scorePercentage = analysis ? Math.round(analysis.score * 100) : 0;

  const getScoreColor = (score: number) => {
    // Score vem de 0-1, convertemos para 0-100
    const percentage = score * 100;
    if (percentage >= 65) return 'text-green-400';
    if (percentage >= 45) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getScoreBgColor = (score: number) => {
    const percentage = score * 100;
    if (percentage >= 65) return 'bg-green-500';
    if (percentage >= 45) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const formatIndicatorValue = (value: number | null) => {
    if (value === null || value === undefined) return 'N/A';
    return value.toFixed(2);
  };

  return (
    <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-6 shadow-2xl border border-gray-700 hover:border-gray-600 transition-all duration-300 hover:shadow-3xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="text-5xl">{icon}</div>
          <div>
            <h2 className="text-2xl font-bold text-white">{symbol}</h2>
            <p className="text-gray-400 text-sm">{name}</p>
          </div>
        </div>
      </div>

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 mb-4"
      >
        <BarChart3 className="w-5 h-5" />
        <span>{loading ? 'Analisando...' : 'Analisar agora'}</span>
      </button>

      {/* Error Message */}
      {error && (
        <div className="bg-red-900/30 border border-red-500/50 rounded-lg p-4 mb-4 flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-red-300 text-sm font-medium">Erro ao analisar</p>
            <p className="text-red-400 text-xs mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Analysis Results */}
      {analysis && (
        <div className="space-y-4 animate-fadeIn">
          {/* Score Section */}
          <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-200">Score de Análise</h3>
              <span className={`text-3xl font-bold ${getScoreColor(analysis.score)}`}>
                {scorePercentage}
              </span>
            </div>
            
            {/* Progress Bar */}
            <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
              <div
                className={`h-full ${getScoreBgColor(analysis.score)} transition-all duration-500 ease-out rounded-full`}
                style={{ width: `${scorePercentage}%` }}
              />
            </div>
            
            <div className="flex items-center justify-between mt-2 text-xs text-gray-400">
              <span>0 = Baixista • 100 = Altista</span>
              <span>{new Date().toLocaleTimeString('pt-BR')}</span>
            </div>
          </div>

          {/* AI Comment - Priority if available */}
          {analysis.ai_comment && (
            <div className="bg-gradient-to-br from-purple-900/30 to-blue-900/30 border border-purple-500/30 rounded-xl p-5">
              <div className="flex items-center space-x-2 mb-3">
                <div className="relative">
                  <div className="absolute inset-0 bg-purple-500 rounded-full blur-sm opacity-50"></div>
                  <div className="relative text-xl">🤖</div>
                </div>
                <h3 className="text-lg font-semibold text-purple-200">Análise IA</h3>
              </div>
              <p className="text-purple-100 text-sm leading-relaxed italic">"{analysis.ai_comment}"</p>
            </div>
          )}

          {/* Diagnostic */}
          <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
            <h3 className="text-lg font-semibold text-gray-200 mb-2">Diagnóstico Técnico</h3>
            <p className="text-gray-300 text-sm leading-relaxed">{analysis.diagnostic}</p>
          </div>

          {/* Indicadores Técnicos - Timeframe Diário */}
          {analysis.indicators && analysis.indicators['1d'] && (
            <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
              <h3 className="text-lg font-semibold text-gray-200 mb-4">Indicadores Técnicos (Diário)</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="bg-gray-900/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400 mb-1">RSI</p>
                  <p className="text-lg font-bold text-white">{formatIndicatorValue(analysis.indicators['1d'].rsi)}</p>
                </div>
                <div className="bg-gray-900/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400 mb-1">EMA 9</p>
                  <p className="text-lg font-bold text-white">{formatIndicatorValue(analysis.indicators['1d'].ema9)}</p>
                </div>
                <div className="bg-gray-900/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400 mb-1">EMA 21</p>
                  <p className="text-lg font-bold text-white">{formatIndicatorValue(analysis.indicators['1d'].ema21)}</p>
                </div>
                <div className="bg-gray-900/50 rounded-lg p-3">
                  <p className="text-xs text-gray-400 mb-1">MACD</p>
                  <p className="text-lg font-bold text-white">{formatIndicatorValue(analysis.indicators['1d'].macd)}</p>
                </div>
              </div>
            </div>
          )}

          {/* Timeframes */}
          {analysis.timeframes && analysis.timeframes.length > 0 && (
            <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
              <h3 className="text-lg font-semibold text-gray-200 mb-3">Timeframes Analisados</h3>
              <div className="flex space-x-2">
                {analysis.timeframes.map((tf) => (
                  <span 
                    key={tf} 
                    className="bg-blue-500/20 border border-blue-500/30 text-blue-300 px-3 py-1 rounded-full text-xs font-medium"
                  >
                    {tf}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CryptoCard;

