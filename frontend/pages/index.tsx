import { useState } from 'react';
import Head from 'next/head';
import CryptoCard from '@/components/CryptoCard';
import { Activity, Sparkles, ArrowLeft, GitCompare } from 'lucide-react';

type ViewMode = 'home' | 'single' | 'compare';

interface CryptoData {
  symbol: string;
  name: string;
  icon: string;
}

export default function Home() {
  const [viewMode, setViewMode] = useState<ViewMode>('home');
  const [selectedCrypto, setSelectedCrypto] = useState<CryptoData | null>(null);
  const [compareMode, setCompareMode] = useState(false);
  const [selectedCryptos, setSelectedCryptos] = useState<CryptoData[]>([]);

  const cryptos: CryptoData[] = [
    { symbol: 'BTC', name: 'Bitcoin', icon: '₿' },
    { symbol: 'ETH', name: 'Ethereum', icon: 'Ξ' },
    { symbol: 'SOL', name: 'Solana', icon: '◎' },
  ];

  const handleSelectCrypto = (crypto: CryptoData) => {
    if (compareMode) {
      // Modo comparação: seleciona até 2 ativos
      if (selectedCryptos.find(c => c.symbol === crypto.symbol)) {
        setSelectedCryptos(selectedCryptos.filter(c => c.symbol !== crypto.symbol));
      } else if (selectedCryptos.length < 2) {
        setSelectedCryptos([...selectedCryptos, crypto]);
      }
    } else {
      // Modo individual
      setSelectedCrypto(crypto);
      setViewMode('single');
    }
  };

  const handleStartCompare = () => {
    if (selectedCryptos.length === 2) {
      setViewMode('compare');
    }
  };

  const handleBackToHome = () => {
    setViewMode('home');
    setSelectedCrypto(null);
    setSelectedCryptos([]);
    setCompareMode(false);
  };

  const toggleCompareMode = () => {
    setCompareMode(!compareMode);
    setSelectedCryptos([]);
  };

  return (
    <>
      <Head>
        <title>Crypto Insight AI - Análise Inteligente de Criptomoedas</title>
        <meta name="description" content="Análise avançada de criptomoedas com IA" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black">
        {/* Background decorative elements */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
        </div>

        <div className="relative z-10 container mx-auto px-3 sm:px-4 md:px-6 lg:px-8 py-6 sm:py-8 md:py-10 lg:py-12">
          {/* Botão Voltar */}
          {viewMode !== 'home' && (
            <button
              onClick={handleBackToHome}
              className="mb-4 sm:mb-6 flex items-center space-x-2 text-sm sm:text-base text-gray-400 hover:text-white transition-colors duration-200 group"
            >
              <ArrowLeft className="w-4 h-4 sm:w-5 sm:h-5 group-hover:-translate-x-1 transition-transform duration-200" />
              <span className="font-medium">Voltar</span>
            </button>
          )}

          {/* HOME VIEW - Seleção de Criptomoedas */}
          {viewMode === 'home' && (
            <>
              {/* Header */}
              <header className="text-center mb-8 sm:mb-12 md:mb-16 pt-2 sm:pt-4 md:pt-6">
                <div className="flex items-center justify-center space-x-2 sm:space-x-3 mb-4 sm:mb-6">
                  <div className="relative">
                    <Sparkles className="w-8 h-8 sm:w-10 sm:h-10 md:w-12 md:h-12 text-blue-400 animate-pulse" />
                    <Activity className="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-purple-400 absolute -top-1 -right-1" />
                  </div>
                </div>
                
                <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold mb-3 sm:mb-4 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent px-3 sm:px-4">
                  Crypto Insight AI
                </h1>
                
                <p className="text-base sm:text-lg md:text-xl lg:text-2xl text-gray-400 font-light mb-2 px-3 sm:px-4">
                  Análise Inteligente de Criptomoedas
                </p>
                
                <p className="text-xs sm:text-sm text-gray-500 max-w-2xl mx-auto px-3 sm:px-4 leading-relaxed">
                  Obtenha análises técnicas avançadas em tempo real com indicadores de mercado, 
                  scores de confiança e recomendações inteligentes
                </p>

                {/* Feature badges */}
                <div className="flex items-center justify-center flex-wrap gap-2 mt-4 sm:mt-6 md:mt-8 px-3 sm:px-4">
                  <span className="bg-blue-500/10 border border-blue-500/30 text-blue-300 px-2.5 sm:px-3 md:px-4 py-1 sm:py-1.5 md:py-2 rounded-full text-xs font-medium whitespace-nowrap">
                    ⚡ Tempo Real
                  </span>
                  <span className="bg-purple-500/10 border border-purple-500/30 text-purple-300 px-2.5 sm:px-3 md:px-4 py-1 sm:py-1.5 md:py-2 rounded-full text-xs font-medium whitespace-nowrap">
                    🎯 Indicadores
                  </span>
                  <span className="bg-pink-500/10 border border-pink-500/30 text-pink-300 px-2.5 sm:px-3 md:px-4 py-1 sm:py-1.5 md:py-2 rounded-full text-xs font-medium whitespace-nowrap">
                    🤖 IA
                  </span>
                </div>
              </header>

              {/* Seleção de Modo */}
              <div className="max-w-3xl mx-auto mb-6 sm:mb-8">
                <div className="text-center mb-4 sm:mb-6">
                  <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-white mb-2 px-3">
                    {compareMode ? 'Selecione dois ativos para comparar' : 'Selecione um ativo para análise'}
                  </h2>
                  <p className="text-gray-400 text-xs sm:text-sm">
                    {compareMode ? `${selectedCryptos.length}/2 selecionados` : 'Clique em um ativo para começar'}
                  </p>
                </div>

                {/* Toggle Compare Mode */}
                <div className="flex justify-center mb-6 sm:mb-8">
                  <button
                    onClick={toggleCompareMode}
                    className={`flex items-center space-x-2 px-4 sm:px-6 py-2.5 sm:py-3 rounded-xl text-sm sm:text-base font-semibold transition-all duration-200 ${
                      compareMode
                        ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                        : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                    }`}
                  >
                    <GitCompare className="w-4 h-4 sm:w-5 sm:h-5" />
                    <span className="whitespace-nowrap">{compareMode ? 'Modo Comparação Ativo' : 'Comparar Ativos'}</span>
                  </button>
                </div>

                {/* Crypto Selection Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
                  {cryptos.map((crypto) => {
                    const isSelected = compareMode && selectedCryptos.find(c => c.symbol === crypto.symbol);
                    return (
                      <button
                        key={crypto.symbol}
                        onClick={() => handleSelectCrypto(crypto)}
                        className={`relative overflow-hidden group bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl sm:rounded-2xl p-6 sm:p-8 shadow-2xl border-2 transition-all duration-300 hover:scale-105 active:scale-100 ${
                          isSelected
                            ? 'border-purple-500 shadow-purple-500/50'
                            : 'border-gray-700 hover:border-blue-500 hover:shadow-blue-500/20'
                        }`}
                      >
                        {/* Fundo animado */}
                        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        
                        <div className="relative z-10">
                          <div className="text-5xl sm:text-6xl mb-3 sm:mb-4">{crypto.icon}</div>
                          <h3 className="text-xl sm:text-2xl font-bold text-white mb-1">{crypto.symbol}</h3>
                          <p className="text-gray-400 text-xs sm:text-sm">{crypto.name}</p>
                          
                          {isSelected && (
                            <div className="mt-3 sm:mt-4 bg-purple-500/20 border border-purple-500/50 rounded-lg px-2.5 sm:px-3 py-1 text-purple-300 text-xs font-semibold inline-block">
                              ✓ Selecionado
                            </div>
                          )}
                        </div>
                      </button>
                    );
                  })}
                </div>

                {/* Botão Iniciar Comparação */}
                {compareMode && selectedCryptos.length === 2 && (
                  <div className="mt-6 sm:mt-8 text-center">
                    <button
                      onClick={handleStartCompare}
                      className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white text-sm sm:text-base font-bold py-3 sm:py-4 px-6 sm:px-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200"
                    >
                      Comparar {selectedCryptos[0].symbol} vs {selectedCryptos[1].symbol}
                    </button>
                  </div>
                )}
              </div>

              {/* Footer */}
              <footer className="mt-10 sm:mt-16 md:mt-20 text-center text-gray-600 text-xs sm:text-sm px-3 sm:px-4">
                <div className="border-t border-gray-800 pt-4 sm:pt-6 md:pt-8 max-w-4xl mx-auto">
                  <p className="mb-2 leading-relaxed">
                    ⚠️ As análises fornecidas são apenas para fins informativos e não constituem aconselhamento financeiro.
                  </p>
                  <p className="text-gray-700 text-xs">
                    Desenvolvido com Next.js, TypeScript e Tailwind CSS • {new Date().getFullYear()}
                  </p>
                </div>
              </footer>
            </>
          )}

          {/* SINGLE VIEW - Análise Individual */}
          {viewMode === 'single' && selectedCrypto && (
            <div className="max-w-5xl mx-auto">
              <CryptoCard
                symbol={selectedCrypto.symbol}
                name={selectedCrypto.name}
                icon={selectedCrypto.icon}
              />
            </div>
          )}

          {/* COMPARE VIEW - Comparação de Dois Ativos */}
          {viewMode === 'compare' && selectedCryptos.length === 2 && (
            <div>
              <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-center text-white mb-4 sm:mb-6 md:mb-8 px-3">
                Comparação: {selectedCryptos[0].symbol} vs {selectedCryptos[1].symbol}
              </h2>
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 sm:gap-6 max-w-7xl mx-auto">
                {selectedCryptos.map((crypto) => (
                  <div key={crypto.symbol} className="w-full">
                    <CryptoCard
                      symbol={crypto.symbol}
                      name={crypto.name}
                      icon={crypto.icon}
                    />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </>
  );
}

