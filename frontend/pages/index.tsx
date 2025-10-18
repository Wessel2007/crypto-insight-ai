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

        <div className="relative z-10 container mx-auto px-4 py-12">
          {/* Header */}
          <header className="text-center mb-16 pt-8">
            <div className="flex items-center justify-center space-x-3 mb-6">
              <div className="relative">
                <Sparkles className="w-12 h-12 text-blue-400 animate-pulse" />
                <Activity className="w-6 h-6 text-purple-400 absolute -top-1 -right-1" />
              </div>
            </div>
            
            <h1 className="text-6xl md:text-7xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              Crypto Insight AI
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-400 font-light mb-2">
              Análise Inteligente de Criptomoedas
            </p>
            
            <p className="text-sm text-gray-500 max-w-2xl mx-auto">
              Obtenha análises técnicas avançadas em tempo real com indicadores de mercado, 
              scores de confiança e recomendações inteligentes
            </p>

            {/* Feature badges */}
            <div className="flex items-center justify-center flex-wrap gap-3 mt-8">
              <span className="bg-blue-500/10 border border-blue-500/30 text-blue-300 px-4 py-2 rounded-full text-xs font-medium">
                ⚡ Análise em Tempo Real
              </span>
              <span className="bg-purple-500/10 border border-purple-500/30 text-purple-300 px-4 py-2 rounded-full text-xs font-medium">
                🎯 Indicadores Técnicos
              </span>
              <span className="bg-pink-500/10 border border-pink-500/30 text-pink-300 px-4 py-2 rounded-full text-xs font-medium">
                🤖 Recomendações IA
              </span>
            </div>
          </header>

          {/* Crypto Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
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
          <footer className="mt-20 text-center text-gray-600 text-sm">
            <div className="border-t border-gray-800 pt-8 max-w-4xl mx-auto">
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

