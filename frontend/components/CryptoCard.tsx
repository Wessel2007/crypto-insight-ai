import React, { useState } from 'react';
import { TrendingUp, TrendingDown, AlertCircle, Activity, BarChart3, Info, Loader2, Zap, Gauge } from 'lucide-react';
import { analyzeCrypto, AnalysisResponse } from '@/lib/api';
import CandlestickChart from './CandlestickChart';
import { indicatorDescriptions, interpretRSI, interpretMFI, interpretADX, interpretStochRSI } from '@/lib/indicatorDescriptions';

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
      // Força nova requisição à API, sem reusar cache
      const data = await analyzeCrypto(symbol);
      // Substitui completamente os dados anteriores
      setAnalysis(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
      // Limpa análise anterior em caso de erro
      setAnalysis(null);
    } finally {
      setLoading(false);
    }
  };

  // Converte score de 0-1 para 0-100 para exibição
  const scorePercentage = analysis ? Math.round(analysis.score * 100) : 0;

  // Função utilitária consolidada para cores baseadas no score
  const getScoreColors = (score: number) => {
    const percentage = score * 100;
    if (percentage >= 65) {
      return {
        text: 'text-green-400',
        bg: 'bg-green-500',
        gradient: 'from-green-900/40 to-emerald-900/40',
        border: 'border-green-500/50'
      };
    }
    if (percentage >= 45) {
      return {
        text: 'text-yellow-400',
        bg: 'bg-yellow-500',
        gradient: 'from-yellow-900/40 to-orange-900/40',
        border: 'border-yellow-500/50'
      };
    }
    return {
      text: 'text-red-400',
      bg: 'bg-red-500',
      gradient: 'from-red-900/40 to-rose-900/40',
      border: 'border-red-500/50'
    };
  };

  const scoreColors = analysis ? getScoreColors(analysis.score) : getScoreColors(0.5);

  const formatIndicatorValue = (value: number | null) => {
    if (value === null || value === undefined) return 'N/A';
    return value.toFixed(2);
  };

  // Componente para exibir indicador com descrição integrada
  const IndicatorCard: React.FC<{
    label: string;
    value: number | null;
    indicatorKey: string;
    interpretation?: string;
    isImportant?: boolean;
  }> = ({ label, value, indicatorKey, interpretation, isImportant = false }) => {
    const indicator = indicatorDescriptions[indicatorKey];
    const description = indicator?.description || "";

    return (
      <div className={`rounded-lg p-3 sm:p-4 transition-all duration-200 overflow-hidden ${
        isImportant 
          ? 'bg-gradient-to-br from-blue-900/40 to-purple-900/40 border-2 border-blue-500/50 shadow-lg shadow-blue-500/20' 
          : 'bg-gray-900/50 border border-gray-700/50'
      }`}>
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1 min-w-0">
            <p className={`text-xs sm:text-sm font-semibold mb-1 break-words ${isImportant ? 'text-blue-300' : 'text-gray-300'}`}>
              {label}
              {isImportant && <span className="ml-1 sm:ml-2 text-xs bg-blue-500/30 text-blue-200 px-1.5 sm:px-2 py-0.5 rounded-full whitespace-nowrap">★ Importante</span>}
            </p>
            <p className={`text-xl sm:text-2xl font-bold truncate ${isImportant ? 'text-white' : 'text-gray-100'}`}>
              {formatIndicatorValue(value)}
            </p>
            {interpretation && (
              <p className={`text-xs mt-1 font-medium break-words ${
                interpretation.includes('Sobrevendido') || interpretation.includes('compra') 
                  ? 'text-green-400' 
                  : interpretation.includes('Sobrecomprado') || interpretation.includes('venda')
                  ? 'text-red-400'
                  : 'text-yellow-400'
              }`}>
                {interpretation}
              </p>
            )}
          </div>
        </div>
        {description && (
          <div className="mt-2 sm:mt-3 pt-2 sm:pt-3 border-t border-gray-700/50">
            <p className="text-xs text-gray-400 leading-relaxed break-words">{description}</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl sm:rounded-2xl p-3 sm:p-4 md:p-5 lg:p-6 shadow-2xl border border-gray-700 transition-all duration-300 w-full overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between mb-4 sm:mb-6">
        <div className="flex items-center space-x-2 sm:space-x-3">
          <div className="text-3xl sm:text-4xl md:text-5xl flex-shrink-0">{icon}</div>
          <div className="overflow-hidden min-w-0">
            <h2 className="text-lg sm:text-xl md:text-2xl font-bold text-white truncate">{symbol}</h2>
            <p className="text-gray-400 text-xs sm:text-sm truncate">{name}</p>
          </div>
        </div>
      </div>

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white text-sm sm:text-base font-semibold py-3 sm:py-4 px-4 sm:px-6 rounded-lg sm:rounded-xl transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center space-x-2 mb-3 sm:mb-4 shadow-lg hover:shadow-xl active:scale-95"
      >
        {loading ? (
          <>
            <Loader2 className="w-4 h-4 sm:w-5 sm:h-5 animate-spin" />
            <span>Analisando...</span>
          </>
        ) : (
          <>
            <BarChart3 className="w-4 h-4 sm:w-5 sm:h-5" />
            <span>Analisar agora</span>
          </>
        )}
      </button>

      {/* Loading Indicator */}
      {loading && (
        <div className="mb-3 sm:mb-4 bg-gradient-to-r from-blue-900/30 to-purple-900/30 border border-blue-500/30 rounded-lg sm:rounded-xl p-4 sm:p-6">
          <div className="flex flex-col items-center space-y-3 sm:space-y-4">
            <div className="relative">
              <div className="w-12 h-12 sm:w-16 sm:h-16 border-4 border-blue-500/30 rounded-full"></div>
              <div className="absolute top-0 left-0 w-12 h-12 sm:w-16 sm:h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <div className="text-center">
              <p className="text-blue-300 text-sm sm:text-base font-semibold mb-1">Processando análise técnica</p>
              <p className="text-blue-400/70 text-xs sm:text-sm">Calculando indicadores e scores...</p>
            </div>
            {/* Progress bar animation */}
            <div className="w-full bg-gray-800 rounded-full h-1.5 sm:h-2 overflow-hidden">
              <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full animate-pulse" style={{ width: '70%' }}></div>
            </div>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-900/30 border border-red-500/50 rounded-lg p-3 sm:p-4 mb-3 sm:mb-4 flex items-start space-x-2 sm:space-x-3">
          <AlertCircle className="w-4 h-4 sm:w-5 sm:h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <div className="min-w-0">
            <p className="text-red-300 text-xs sm:text-sm font-medium">Erro ao analisar</p>
            <p className="text-red-400 text-xs mt-1 break-words">{error}</p>
          </div>
        </div>
      )}

      {/* Analysis Results */}
      {analysis && (
        <div className="space-y-3 sm:space-y-4 animate-fadeIn">
          {/* Timestamp da última análise - usando dados reais do backend */}
          {analysis.last_candle_timestamp && analysis.last_candle_timestamp !== 'N/A' && (
            <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-2.5 sm:p-3 mb-2">
              <div className="flex items-center justify-center space-x-1.5 sm:space-x-2">
                <Activity className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-blue-400 flex-shrink-0 animate-pulse" />
                <div className="text-center flex-1">
                  <p className="text-xs text-gray-400 mb-0.5">Dados do mercado atualizados:</p>
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-center gap-1 sm:gap-3">
                    <p className="text-sm sm:text-base font-semibold text-blue-300">
                      {analysis.last_candle_timestamp}
                    </p>
                    {analysis.last_candle_timestamp_brt && analysis.last_candle_timestamp_brt !== 'N/A' && (
                      <>
                        <span className="hidden sm:inline text-gray-500">|</span>
                        <p className="text-xs sm:text-sm font-medium text-green-300">
                          {analysis.last_candle_timestamp_brt}
                        </p>
                      </>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Score Section - Com cores dinâmicas */}
          <div className={`rounded-lg sm:rounded-xl p-4 sm:p-5 md:p-6 border-2 shadow-xl transition-all duration-500 bg-gradient-to-br ${scoreColors.gradient} ${scoreColors.border}`}>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-3 sm:mb-4 gap-3">
              <h3 className={`text-base sm:text-lg font-semibold ${
                scorePercentage >= 65 
                  ? 'text-green-200'
                  : scorePercentage >= 45
                  ? 'text-yellow-200'
                  : 'text-red-200'
              }`}>
                Score de Análise
              </h3>
              <div className="text-center sm:text-right">
                <span className={`text-3xl sm:text-4xl font-bold ${scoreColors.text}`}>
                  {scorePercentage}
                </span>
                <p className="text-xs text-gray-400 mt-1 whitespace-nowrap">
                  {scorePercentage >= 65 
                    ? '🟢 Momento favorável'
                    : scorePercentage >= 45
                    ? '🟡 Neutro'
                    : '🔴 Momento desfavorável'}
                </p>
              </div>
            </div>
            
            {/* Progress Bar - Destaque visual */}
            <div className="w-full bg-gray-900/60 rounded-full h-3 sm:h-4 overflow-hidden shadow-inner">
              <div
                className={`h-full ${scoreColors.bg} transition-all duration-700 ease-out rounded-full shadow-lg relative`}
                style={{ width: `${scorePercentage}%` }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
              </div>
            </div>
            
            <div className="flex items-center justify-between mt-2 sm:mt-3 text-xs text-gray-400 gap-2">
              <span className="flex items-center space-x-1 whitespace-nowrap">
                <span className="inline-block w-1.5 h-1.5 sm:w-2 sm:h-2 bg-red-500 rounded-full flex-shrink-0"></span>
                <span className="hidden sm:inline">0 Baixista</span>
                <span className="sm:hidden">0</span>
              </span>
              <span className="flex items-center space-x-1 whitespace-nowrap">
                <span className="inline-block w-1.5 h-1.5 sm:w-2 sm:h-2 bg-yellow-500 rounded-full flex-shrink-0"></span>
                <span className="hidden sm:inline">50 Neutro</span>
                <span className="sm:hidden">50</span>
              </span>
              <span className="flex items-center space-x-1 whitespace-nowrap">
                <span className="inline-block w-1.5 h-1.5 sm:w-2 sm:h-2 bg-green-500 rounded-full flex-shrink-0"></span>
                <span className="hidden sm:inline">100 Altista</span>
                <span className="sm:hidden">100</span>
              </span>
            </div>
          </div>

          {/* AI Comment - Priority if available */}
          {analysis.ai_comment && (
            <div className="bg-gradient-to-br from-purple-900/40 to-blue-900/40 border-2 border-purple-500/40 rounded-lg sm:rounded-xl p-3 sm:p-4 md:p-5 shadow-lg overflow-hidden">
              <div className="flex items-center space-x-2 mb-2 sm:mb-3">
                <div className="relative flex-shrink-0">
                  <div className="absolute inset-0 bg-purple-500 rounded-full blur-md opacity-60 animate-pulse-glow"></div>
                  <div className="relative text-lg sm:text-xl md:text-2xl">🤖</div>
                </div>
                <h3 className="text-sm sm:text-base md:text-lg font-semibold text-purple-200 truncate">Análise da IA</h3>
              </div>
              <p className="text-purple-100 text-xs sm:text-sm leading-relaxed italic break-words">"{analysis.ai_comment}"</p>
            </div>
          )}

          {/* Trade Opportunity - Quick Trade Analysis - DESTAQUE */}
          {analysis.trade_opportunity && (
            <div className={`rounded-xl p-4 sm:p-6 border-2 shadow-2xl transition-all duration-500 overflow-hidden ${
              analysis.trade_opportunity.probability >= 0.7 
                ? 'bg-gradient-to-br from-green-900/40 to-emerald-900/40 border-green-500/60 shadow-green-500/20'
                : analysis.trade_opportunity.probability >= 0.4
                ? 'bg-gradient-to-br from-yellow-900/40 to-orange-900/40 border-yellow-500/60 shadow-yellow-500/20'
                : 'bg-gradient-to-br from-gray-900/40 to-slate-900/40 border-gray-500/60 shadow-gray-500/20'
            }`}>
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4 gap-3">
                <div className="flex items-center space-x-3 min-w-0">
                  <div className="relative flex-shrink-0">
                    <div className={`absolute inset-0 rounded-full blur-md opacity-60 ${
                      analysis.trade_opportunity.probability >= 0.7 
                        ? 'bg-green-500'
                        : analysis.trade_opportunity.probability >= 0.4
                        ? 'bg-yellow-500'
                        : 'bg-gray-500'
                    }`}></div>
                    <div className="relative text-2xl">
                      {analysis.trade_opportunity.probability >= 0.7 ? '⚡' : 
                       analysis.trade_opportunity.probability >= 0.4 ? '⏱️' : '⏸️'}
                    </div>
                  </div>
                  <div className="min-w-0">
                    <h3 className={`text-lg font-bold truncate ${
                      analysis.trade_opportunity.probability >= 0.7 
                        ? 'text-green-200'
                        : analysis.trade_opportunity.probability >= 0.4
                        ? 'text-yellow-200'
                        : 'text-gray-200'
                    }`}>
                      Trade Rápido (1h)
                    </h3>
                    <p className="text-xs text-gray-400 truncate">Probabilidade de sucesso</p>
                  </div>
                </div>
                <div className="text-center sm:text-right flex-shrink-0">
                  <div className={`text-4xl sm:text-5xl font-bold ${
                    analysis.trade_opportunity.probability >= 0.7 
                      ? 'text-green-400'
                      : analysis.trade_opportunity.probability >= 0.4
                      ? 'text-yellow-400'
                      : 'text-gray-400'
                  }`}>
                    {Math.round(analysis.trade_opportunity.probability * 100)}%
                  </div>
                </div>
              </div>
              
              {/* Progress Bar - DESTAQUE MÁXIMO */}
              <div className="mb-3 sm:mb-4">
                <div className="flex items-center justify-between mb-1.5 sm:mb-2 text-xs text-gray-400">
                  <span>0%</span>
                  <span className="font-semibold text-xs sm:text-sm">Probabilidade</span>
                  <span>100%</span>
                </div>
                <div className="w-full bg-gray-900/60 rounded-full h-5 sm:h-6 overflow-hidden shadow-inner">
                  <div
                    className={`h-full transition-all duration-700 ease-out rounded-full shadow-lg relative ${
                      analysis.trade_opportunity.probability >= 0.7 
                        ? 'bg-gradient-to-r from-green-500 to-emerald-400'
                        : analysis.trade_opportunity.probability >= 0.4
                        ? 'bg-gradient-to-r from-yellow-500 to-orange-400'
                        : 'bg-gradient-to-r from-gray-500 to-slate-400'
                    }`}
                    style={{ width: `${analysis.trade_opportunity.probability * 100}%` }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer"></div>
                    <div className="absolute right-1.5 sm:right-2 top-1/2 -translate-y-1/2 text-xs font-bold text-white">
                      {Math.round(analysis.trade_opportunity.probability * 100)}%
                    </div>
                  </div>
                </div>
              </div>
              
              <p className={`text-sm leading-relaxed mb-3 break-words ${
                analysis.trade_opportunity.probability >= 0.7 
                  ? 'text-green-100'
                  : analysis.trade_opportunity.probability >= 0.4
                  ? 'text-yellow-100'
                  : 'text-gray-100'
              }`}>
                {analysis.trade_opportunity.comment}
              </p>
              
              {/* Indicador visual de ação */}
              <div className={`pt-3 border-t ${
                analysis.trade_opportunity.probability >= 0.7 
                  ? 'border-green-500/30'
                  : analysis.trade_opportunity.probability >= 0.4
                  ? 'border-yellow-500/30'
                  : 'border-gray-500/30'
              }`}>
                <div className="flex flex-col sm:flex-row items-center justify-between text-xs gap-2">
                  <span className="text-gray-400 text-center sm:text-left">Baseado em 5 critérios técnicos</span>
                  <span className={`font-semibold px-3 py-1.5 rounded-lg shadow-md text-center whitespace-nowrap ${
                    analysis.trade_opportunity.probability >= 0.7 
                      ? 'bg-green-500/30 text-green-200 border border-green-500/50'
                      : analysis.trade_opportunity.probability >= 0.4
                      ? 'bg-yellow-500/30 text-yellow-200 border border-yellow-500/50'
                      : 'bg-gray-500/30 text-gray-200 border border-gray-500/50'
                  }`}>
                    {analysis.trade_opportunity.probability >= 0.7 
                      ? '🟢 Sinal Forte'
                      : analysis.trade_opportunity.probability >= 0.4
                      ? '🟡 Aguardar'
                      : '🔴 Sem Sinal'}
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
              isLoading={loading}
            />
          )}

          {/* Diagnostic */}
          <div className="bg-gray-800/50 rounded-lg sm:rounded-xl p-3 sm:p-4 md:p-5 border border-gray-700 overflow-hidden">
            <h3 className="text-sm sm:text-base md:text-lg font-semibold text-gray-200 mb-2">Diagnóstico Técnico</h3>
            <p className="text-gray-300 text-xs sm:text-sm leading-relaxed break-words">{analysis.diagnostic}</p>
          </div>

          {/* Indicadores Técnicos - Timeframe Diário */}
          {analysis.indicators && analysis.indicators['1d'] && (
            <div className="space-y-4 sm:space-y-5 md:space-y-6">
              <div className="border-l-4 border-blue-500 pl-3 sm:pl-4">
                <h2 className="text-lg sm:text-xl font-bold text-gray-100 mb-1">📊 Indicadores Técnicos</h2>
                <p className="text-xs sm:text-sm text-gray-400">Análise detalhada com descrições educacionais</p>
              </div>

              {/* Tendência */}
              <div className="bg-gradient-to-br from-gray-800/80 to-gray-900/80 rounded-lg sm:rounded-xl p-3 sm:p-4 md:p-5 border border-blue-500/30">
                <div className="flex items-center mb-3 sm:mb-4 md:mb-5 pb-2 sm:pb-3 border-b border-blue-500/20">
                  <TrendingUp className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-blue-400 flex-shrink-0" />
                  <h3 className="text-base sm:text-lg font-bold text-blue-300">Tendência</h3>
                  <span className="ml-auto text-xs text-gray-400 whitespace-nowrap">Médias Móveis</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 sm:gap-3">
                  <IndicatorCard 
                    label="EMA 9" 
                    value={analysis.indicators['1d'].trend.EMA9} 
                    indicatorKey="EMA9" 
                    isImportant={true}
                  />
                  <IndicatorCard 
                    label="EMA 21" 
                    value={analysis.indicators['1d'].trend.EMA21} 
                    indicatorKey="EMA21" 
                    isImportant={true}
                  />
                  <IndicatorCard 
                    label="EMA 50" 
                    value={analysis.indicators['1d'].trend.EMA50} 
                    indicatorKey="EMA50" 
                  />
                  <IndicatorCard 
                    label="EMA 200" 
                    value={analysis.indicators['1d'].trend.EMA200} 
                    indicatorKey="EMA200" 
                  />
                  <IndicatorCard 
                    label="SMA 100" 
                    value={analysis.indicators['1d'].trend.SMA100} 
                    indicatorKey="SMA100" 
                  />
                </div>
              </div>

              {/* Momentum */}
              <div className="bg-gradient-to-br from-gray-800/80 to-gray-900/80 rounded-lg sm:rounded-xl p-3 sm:p-4 md:p-5 border border-purple-500/30">
                <div className="flex items-center mb-3 sm:mb-4 md:mb-5 pb-2 sm:pb-3 border-b border-purple-500/20">
                  <Zap className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-purple-400 flex-shrink-0" />
                  <h3 className="text-base sm:text-lg font-bold text-purple-300">Momentum</h3>
                  <span className="ml-auto text-xs text-gray-400 whitespace-nowrap hidden sm:inline">Força do Movimento</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 sm:gap-3">
                  <IndicatorCard 
                    label="RSI (14)" 
                    value={analysis.indicators['1d'].momentum.RSI} 
                    indicatorKey="RSI"
                    interpretation={interpretRSI(analysis.indicators['1d'].momentum.RSI)}
                    isImportant={true}
                  />
                  <IndicatorCard 
                    label="MACD" 
                    value={analysis.indicators['1d'].momentum.MACD} 
                    indicatorKey="MACD" 
                    isImportant={true}
                  />
                  <IndicatorCard 
                    label="MACD Signal" 
                    value={analysis.indicators['1d'].momentum.MACD_Signal} 
                    indicatorKey="MACD_Signal" 
                  />
                  <IndicatorCard 
                    label="MACD Histograma" 
                    value={analysis.indicators['1d'].momentum.MACD_Histogram} 
                    indicatorKey="MACD_Histogram" 
                  />
                  <IndicatorCard 
                    label="Stoch RSI K" 
                    value={analysis.indicators['1d'].momentum.Stochastic_RSI_K} 
                    indicatorKey="Stochastic_RSI_K"
                    interpretation={interpretStochRSI(analysis.indicators['1d'].momentum.Stochastic_RSI_K)}
                  />
                  <IndicatorCard 
                    label="Stoch RSI D" 
                    value={analysis.indicators['1d'].momentum.Stochastic_RSI_D} 
                    indicatorKey="Stochastic_RSI_D"
                  />
                </div>
              </div>

              {/* Volatilidade */}
              <div className="bg-gradient-to-br from-gray-800/80 to-gray-900/80 rounded-lg sm:rounded-xl p-3 sm:p-4 md:p-5 border border-yellow-500/30">
                <div className="flex items-center mb-3 sm:mb-4 md:mb-5 pb-2 sm:pb-3 border-b border-yellow-500/20">
                  <AlertCircle className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-yellow-400 flex-shrink-0" />
                  <h3 className="text-base sm:text-lg font-bold text-yellow-300">Volatilidade</h3>
                  <span className="ml-auto text-xs text-gray-400 whitespace-nowrap hidden sm:inline">Risco e Variação</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-3">
                  <IndicatorCard 
                    label="ATR (14)" 
                    value={analysis.indicators['1d'].volatility.ATR} 
                    indicatorKey="ATR" 
                  />
                  <IndicatorCard 
                    label="Bollinger Superior" 
                    value={analysis.indicators['1d'].volatility.BB_Upper} 
                    indicatorKey="BB_Upper" 
                  />
                  <IndicatorCard 
                    label="Bollinger Média" 
                    value={analysis.indicators['1d'].volatility.BB_Middle} 
                    indicatorKey="BB_Middle" 
                  />
                  <IndicatorCard 
                    label="Bollinger Inferior" 
                    value={analysis.indicators['1d'].volatility.BB_Lower} 
                    indicatorKey="BB_Lower" 
                  />
                </div>
              </div>

              {/* Volume e Força */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 sm:gap-4">
                {/* Volume */}
                <div className="bg-gradient-to-br from-gray-800/80 to-gray-900/80 rounded-lg sm:rounded-xl p-3 sm:p-4 md:p-5 border border-green-500/30">
                  <div className="flex items-center mb-3 sm:mb-4 md:mb-5 pb-2 sm:pb-3 border-b border-green-500/20">
                    <BarChart3 className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-green-400 flex-shrink-0" />
                    <h3 className="text-base sm:text-lg font-bold text-green-300">Volume</h3>
                    <span className="ml-auto text-xs text-gray-400">Liquidez</span>
                  </div>
                  <div className="space-y-3 sm:space-y-4">
                    <IndicatorCard 
                      label="Volume MA" 
                      value={analysis.indicators['1d'].volume.Volume_MA} 
                      indicatorKey="Volume_MA" 
                    />
                    <IndicatorCard 
                      label="MFI (14)" 
                      value={analysis.indicators['1d'].volume.MFI} 
                      indicatorKey="MFI"
                      interpretation={interpretMFI(analysis.indicators['1d'].volume.MFI)}
                    />
                    <IndicatorCard 
                      label="OBV" 
                      value={analysis.indicators['1d'].volume.OBV} 
                      indicatorKey="OBV" 
                    />
                  </div>
                </div>

                {/* Força da Tendência */}
                <div className="bg-gradient-to-br from-gray-800/80 to-gray-900/80 rounded-lg sm:rounded-xl p-3 sm:p-4 md:p-5 border border-orange-500/30">
                  <div className="flex items-center mb-3 sm:mb-4 md:mb-5 pb-2 sm:pb-3 border-b border-orange-500/20">
                    <Gauge className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-orange-400 flex-shrink-0" />
                    <h3 className="text-base sm:text-lg font-bold text-orange-300">Força</h3>
                    <span className="ml-auto text-xs text-gray-400">Intensidade</span>
                  </div>
                  <div className="space-y-3 sm:space-y-4">
                    <IndicatorCard 
                      label="ADX (14)" 
                      value={analysis.indicators['1d'].strength.ADX} 
                      indicatorKey="ADX"
                      interpretation={interpretADX(analysis.indicators['1d'].strength.ADX)}
                    />
                    <IndicatorCard 
                      label="Preço Atual" 
                      value={analysis.indicators['1d'].price.last_close} 
                      indicatorKey="last_close" 
                    />
                    <IndicatorCard 
                      label="Volume Atual" 
                      value={analysis.indicators['1d'].price.current_volume} 
                      indicatorKey="current_volume" 
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Timeframes */}
          {analysis.timeframes && analysis.timeframes.length > 0 && (
            <div className="bg-gray-800/50 rounded-lg sm:rounded-xl p-3 sm:p-4 md:p-5 border border-gray-700 overflow-hidden">
              <h3 className="text-sm sm:text-base md:text-lg font-semibold text-gray-200 mb-2 sm:mb-3">Timeframes Analisados</h3>
              <div className="flex flex-wrap gap-1.5 sm:gap-2">
                {analysis.timeframes.map((tf) => (
                  <span 
                    key={tf} 
                    className="bg-blue-500/20 border border-blue-500/30 text-blue-300 px-2 sm:px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap"
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

