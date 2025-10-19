import Head from 'next/head';
import CryptoCard from '@/components/CryptoCard';
import { Activity, Sparkles } from 'lucide-react';

export default function Home() {
  const cryptos = [
    { symbol: 'BTC', name: 'Bitcoin', icon: '₿' },
    { symbol: 'ETH', name: 'Ethereum', icon: 'Ξ' },
    { symbol: 'SOL', name: 'Solana', icon: '◎' },
  ];

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

        <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
          {/* Header */}
          <header className="text-center mb-12 sm:mb-16 pt-4 sm:pt-8">
            <div className="flex items-center justify-center space-x-3 mb-6">
              <div className="relative">
                <Sparkles className="w-10 h-10 sm:w-12 sm:h-12 text-blue-400 animate-pulse" />
                <Activity className="w-5 h-5 sm:w-6 sm:h-6 text-purple-400 absolute -top-1 -right-1" />
              </div>
            </div>
            
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent px-4">
              Crypto Insight AI
            </h1>
            
            <p className="text-lg sm:text-xl md:text-2xl text-gray-400 font-light mb-2 px-4">
              Análise Inteligente de Criptomoedas
            </p>
            
            <p className="text-xs sm:text-sm text-gray-500 max-w-2xl mx-auto px-4">
              Obtenha análises técnicas avançadas em tempo real com indicadores de mercado, 
              scores de confiança e recomendações inteligentes
            </p>

            {/* Feature badges */}
            <div className="flex items-center justify-center flex-wrap gap-2 sm:gap-3 mt-6 sm:mt-8 px-4">
              <span className="bg-blue-500/10 border border-blue-500/30 text-blue-300 px-3 sm:px-4 py-1.5 sm:py-2 rounded-full text-xs font-medium">
                ⚡ Tempo Real
              </span>
              <span className="bg-purple-500/10 border border-purple-500/30 text-purple-300 px-3 sm:px-4 py-1.5 sm:py-2 rounded-full text-xs font-medium">
                🎯 Indicadores
              </span>
              <span className="bg-pink-500/10 border border-pink-500/30 text-pink-300 px-3 sm:px-4 py-1.5 sm:py-2 rounded-full text-xs font-medium">
                🤖 IA
              </span>
            </div>
          </header>

          {/* Crypto Cards Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6 lg:gap-8 max-w-7xl mx-auto">
            {cryptos.map((crypto) => (
              <CryptoCard
                key={crypto.symbol}
                symbol={crypto.symbol}
                name={crypto.name}
                icon={crypto.icon}
              />
            ))}
          </div>

          {/* Footer */}
          <footer className="mt-12 sm:mt-20 text-center text-gray-600 text-xs sm:text-sm px-4">
            <div className="border-t border-gray-800 pt-6 sm:pt-8 max-w-4xl mx-auto">
              <p className="mb-2">
                ⚠️ As análises fornecidas são apenas para fins informativos e não constituem aconselhamento financeiro.
              </p>
              <p className="text-gray-700">
                Desenvolvido com Next.js, TypeScript e Tailwind CSS • {new Date().getFullYear()}
              </p>
            </div>
          </footer>
        </div>
      </main>
    </>
  );
}

