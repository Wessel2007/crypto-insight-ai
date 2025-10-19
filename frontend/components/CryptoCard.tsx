import React, { useState } from 'react';
import { TrendingUp, TrendingDown, AlertCircle, Activity, BarChart3, Info } from 'lucide-react';
import { analyzeCrypto, AnalysisResponse } from '@/lib/api';
import CandlestickChart from './CandlestickChart';
import { getIndicatorDescription, interpretRSI, interpretMFI, interpretADX, interpretStochRSI } from '@/lib/indicatorDescriptions';

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

  // Componente para exibir indicador com tooltip educacional
  const IndicatorBox: React.FC<{
    label: string;
    value: number | null;
    indicatorKey: string;
    interpretation?: string;
  }> = ({ label, value, indicatorKey, interpretation }) => {
    const [showTooltip, setShowTooltip] = useState(false);
    const description = getIndicatorDescription(indicatorKey);

    return (
      <div className="bg-gray-900/50 rounded-lg p-3 relative group">
        <div className="flex items-center justify-between mb-1">
          <p className="text-xs text-gray-400">{label}</p>
          {description && (
            <button
              onMouseEnter={() => setShowTooltip(true)}
              onMouseLeave={() => setShowTooltip(false)}
              className="text-blue-400 hover:text-blue-300 transition-colors"
            >
              <Info className="w-3 h-3" />
            </button>
          )}
        </div>
        <p className="text-base font-bold text-white">
          {formatIndicatorValue(value)}
          {interpretation && <span className="text-xs ml-1 text-gray-400">{interpretation}</span>}
        </p>
        
        {/* Tooltip educacional */}
        {showTooltip && description && (
          <div className="absolute z-10 bottom-full left-0 mb-2 w-64 bg-gray-900 border border-blue-500/50 rounded-lg p-3 shadow-xl">
            <div className="flex items-start space-x-2">
              <Info className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
              <p className="text-xs text-gray-300 leading-relaxed">{description}</p>
            </div>
            <div className="absolute -bottom-1 left-4 w-2 h-2 bg-gray-900 border-r border-b border-blue-500/50 transform rotate-45"></div>
          </div>
        )}
      </div>
    );
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

          {/* Trade Opportunity - Quick Trade Analysis */}
          {analysis.trade_opportunity && (
            <div className={`rounded-xl p-5 border-2 ${
              analysis.trade_opportunity.probability >= 0.7 
                ? 'bg-gradient-to-br from-green-900/30 to-emerald-900/30 border-green-500/50'
                : analysis.trade_opportunity.probability >= 0.4
                ? 'bg-gradient-to-br from-yellow-900/30 to-orange-900/30 border-yellow-500/50'
                : 'bg-gradient-to-br from-gray-900/30 to-slate-900/30 border-gray-500/50'
            }`}>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <div className="relative">
                    <div className={`absolute inset-0 rounded-full blur-sm opacity-50 ${
                      analysis.trade_opportunity.probability >= 0.7 
                        ? 'bg-green-500'
                        : analysis.trade_opportunity.probability >= 0.4
                        ? 'bg-yellow-500'
                        : 'bg-gray-500'
                    }`}></div>
                    <div className="relative text-xl">
                      {analysis.trade_opportunity.probability >= 0.7 ? '⚡' : 
                       analysis.trade_opportunity.probability >= 0.4 ? '⏱️' : '⏸️'}
                    </div>
                  </div>
                  <h3 className={`text-lg font-semibold ${
                    analysis.trade_opportunity.probability >= 0.7 
                      ? 'text-green-200'
                      : analysis.trade_opportunity.probability >= 0.4
                      ? 'text-yellow-200'
                      : 'text-gray-200'
                  }`}>
                    Oportunidade de Trade Rápido (1h)
                  </h3>
                </div>
                <div className={`text-2xl font-bold ${
                  analysis.trade_opportunity.probability >= 0.7 
                    ? 'text-green-400'
                    : analysis.trade_opportunity.probability >= 0.4
                    ? 'text-yellow-400'
                    : 'text-gray-400'
                }`}>
                  {Math.round(analysis.trade_opportunity.probability * 100)}%
                </div>
              </div>
              
              {/* Progress Bar */}
              <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden mb-3">
                <div
                  className={`h-full transition-all duration-500 ease-out rounded-full ${
                    analysis.trade_opportunity.probability >= 0.7 
                      ? 'bg-green-500'
                      : analysis.trade_opportunity.probability >= 0.4
                      ? 'bg-yellow-500'
                      : 'bg-gray-500'
                  }`}
                  style={{ width: `${analysis.trade_opportunity.probability * 100}%` }}
                />
              </div>
              
              <p className={`text-sm leading-relaxed ${
                analysis.trade_opportunity.probability >= 0.7 
                  ? 'text-green-100'
                  : analysis.trade_opportunity.probability >= 0.4
                  ? 'text-yellow-100'
                  : 'text-gray-100'
              }`}>
                {analysis.trade_opportunity.comment}
              </p>
              
              {/* Indicador visual de ação */}
              <div className={`mt-3 pt-3 border-t ${
                analysis.trade_opportunity.probability >= 0.7 
                  ? 'border-green-500/30'
                  : analysis.trade_opportunity.probability >= 0.4
                  ? 'border-yellow-500/30'
                  : 'border-gray-500/30'
              }`}>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-gray-400">Baseado em 5 critérios técnicos</span>
                  <span className={`font-semibold px-2 py-1 rounded ${
                    analysis.trade_opportunity.probability >= 0.7 
                      ? 'bg-green-500/20 text-green-300'
                      : analysis.trade_opportunity.probability >= 0.4
                      ? 'bg-yellow-500/20 text-yellow-300'
                      : 'bg-gray-500/20 text-gray-300'
                  }`}>
                    {analysis.trade_opportunity.probability >= 0.7 
                      ? '🟢 Sinal Forte'
                      : analysis.trade_opportunity.probability >= 0.4
                      ? '🟡 Aguardar Confirmação'
                      : '🔴 Sem Sinal Claro'}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Candlestick Chart */}
          {analysis.chart_data && analysis.chart_data.candles && analysis.chart_data.candles.length > 0 && (
            <CandlestickChart 
              data={analysis.chart_data.candles} 
              symbol={analysis.symbol}
            />
          )}

          {/* Diagnostic */}
          <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
            <h3 className="text-lg font-semibold text-gray-200 mb-2">Diagnóstico Técnico</h3>
            <p className="text-gray-300 text-sm leading-relaxed">{analysis.diagnostic}</p>
          </div>

          {/* Indicadores Técnicos - Timeframe Diário */}
          {analysis.indicators && analysis.indicators['1d'] && (
            <div className="space-y-4">
              {/* Tendência */}
              <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
                <h3 className="text-lg font-semibold text-blue-300 mb-4 flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2" />
                  Tendência
                </h3>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <IndicatorBox label="EMA 9" value={analysis.indicators['1d'].trend.EMA9} indicatorKey="EMA9" />
                  <IndicatorBox label="EMA 21" value={analysis.indicators['1d'].trend.EMA21} indicatorKey="EMA21" />
                  <IndicatorBox label="EMA 50" value={analysis.indicators['1d'].trend.EMA50} indicatorKey="EMA50" />
                  <IndicatorBox label="EMA 200" value={analysis.indicators['1d'].trend.EMA200} indicatorKey="EMA200" />
                  <IndicatorBox label="SMA 100" value={analysis.indicators['1d'].trend.SMA100} indicatorKey="SMA100" />
                </div>
              </div>

              {/* Momentum */}
              <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
                <h3 className="text-lg font-semibold text-purple-300 mb-4 flex items-center">
                  <Activity className="w-5 h-5 mr-2" />
                  Momentum
                </h3>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <IndicatorBox 
                    label="RSI (14)" 
                    value={analysis.indicators['1d'].momentum.RSI} 
                    indicatorKey="RSI"
                    interpretation={interpretRSI(analysis.indicators['1d'].momentum.RSI)}
                  />
                  <IndicatorBox 
                    label="Stoch RSI K" 
                    value={analysis.indicators['1d'].momentum.Stochastic_RSI_K} 
                    indicatorKey="Stochastic_RSI_K"
                    interpretation={interpretStochRSI(analysis.indicators['1d'].momentum.Stochastic_RSI_K)}
                  />
                  <IndicatorBox 
                    label="Stoch RSI D" 
                    value={analysis.indicators['1d'].momentum.Stochastic_RSI_D} 
                    indicatorKey="Stochastic_RSI_D"
                  />
                  <IndicatorBox label="MACD" value={analysis.indicators['1d'].momentum.MACD} indicatorKey="MACD" />
                  <IndicatorBox label="MACD Signal" value={analysis.indicators['1d'].momentum.MACD_Signal} indicatorKey="MACD_Signal" />
                  <IndicatorBox label="MACD Hist" value={analysis.indicators['1d'].momentum.MACD_Histogram} indicatorKey="MACD_Histogram" />
                </div>
              </div>

              {/* Volatilidade */}
              <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
                <h3 className="text-lg font-semibold text-yellow-300 mb-4 flex items-center">
                  <AlertCircle className="w-5 h-5 mr-2" />
                  Volatilidade
                </h3>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <IndicatorBox label="ATR (14)" value={analysis.indicators['1d'].volatility.ATR} indicatorKey="ATR" />
                  <IndicatorBox label="BB Superior" value={analysis.indicators['1d'].volatility.BB_Upper} indicatorKey="BB_Upper" />
                  <IndicatorBox label="BB Média" value={analysis.indicators['1d'].volatility.BB_Middle} indicatorKey="BB_Middle" />
                  <IndicatorBox label="BB Inferior" value={analysis.indicators['1d'].volatility.BB_Lower} indicatorKey="BB_Lower" />
                </div>
              </div>

              {/* Volume e Força */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Volume */}
                <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
                  <h3 className="text-lg font-semibold text-green-300 mb-4 flex items-center">
                    <BarChart3 className="w-5 h-5 mr-2" />
                    Volume
                  </h3>
                  <div className="space-y-3 text-sm">
                    <IndicatorBox label="Volume MA" value={analysis.indicators['1d'].volume.Volume_MA} indicatorKey="Volume_MA" />
                    <IndicatorBox 
                      label="MFI (14)" 
                      value={analysis.indicators['1d'].volume.MFI} 
                      indicatorKey="MFI"
                      interpretation={interpretMFI(analysis.indicators['1d'].volume.MFI)}
                    />
                    <IndicatorBox label="OBV" value={analysis.indicators['1d'].volume.OBV} indicatorKey="OBV" />
                  </div>
                </div>

                {/* Força */}
                <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
                  <h3 className="text-lg font-semibold text-orange-300 mb-4 flex items-center">
                    <TrendingDown className="w-5 h-5 mr-2" />
                    Força da Tendência
                  </h3>
                  <div className="space-y-3 text-sm">
                    <IndicatorBox 
                      label="ADX (14)" 
                      value={analysis.indicators['1d'].strength.ADX} 
                      indicatorKey="ADX"
                      interpretation={interpretADX(analysis.indicators['1d'].strength.ADX)}
                    />
                    <IndicatorBox label="Preço Atual" value={analysis.indicators['1d'].price.last_close} indicatorKey="last_close" />
                    <IndicatorBox label="Volume Atual" value={analysis.indicators['1d'].price.current_volume} indicatorKey="current_volume" />
                  </div>
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

