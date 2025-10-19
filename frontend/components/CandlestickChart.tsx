import React, { useEffect, useRef } from 'react';
import { createChart, ColorType } from 'lightweight-charts';

interface CandleData {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  ema9?: number | null;
  ema21?: number | null;
  ema200?: number | null;
}

interface CandlestickChartProps {
  data: CandleData[];
  symbol: string;
}

const CandlestickChart: React.FC<CandlestickChartProps> = ({ data, symbol }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!chartContainerRef.current || data.length === 0) return;

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: 'transparent' },
        textColor: '#D1D5DB',
      },
      grid: {
        vertLines: { color: '#374151' },
        horzLines: { color: '#374151' },
      },
      width: chartContainerRef.current.clientWidth,
      height: 500,
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
        borderColor: '#4B5563',
      },
      rightPriceScale: {
        borderColor: '#4B5563',
      },
      crosshair: {
        mode: 1,
      },
    });

    // Série de Candlesticks
    const candleSeries = chart.addCandlestickSeries({
      upColor: '#10B981',
      downColor: '#EF4444',
      borderVisible: false,
      wickUpColor: '#10B981',
      wickDownColor: '#EF4444',
    });

    // Série de Volume (na parte inferior)
    const volumeSeries = chart.addHistogramSeries({
      color: '#3B82F6',
      priceFormat: {
        type: 'volume',
      },
      priceScaleId: 'volume',
    });

    // Configura a escala de volume para ficar em baixo
    chart.priceScale('volume').applyOptions({
      scaleMargins: {
        top: 0.7,
        bottom: 0,
      },
    });

    // Série EMA9 (azul claro)
    const ema9Series = chart.addLineSeries({
      color: '#60A5FA',
      lineWidth: 2,
    });

    // Série EMA21 (laranja)
    const ema21Series = chart.addLineSeries({
      color: '#FB923C',
      lineWidth: 2,
    });

    // Série EMA200 (roxo)
    const ema200Series = chart.addLineSeries({
      color: '#A78BFA',
      lineWidth: 2,
    });

    // Prepara dados das velas
    const candleData = data.map(item => ({
      time: item.time,
      open: item.open,
      high: item.high,
      low: item.low,
      close: item.close,
    }));

    // Prepara dados de volume
    const volumeData = data.map(item => ({
      time: item.time,
      value: item.volume,
      color: item.close >= item.open ? '#10B98166' : '#EF444466',
    }));

    // Prepara dados das EMAs
    const ema9Data = data
      .filter(item => item.ema9 != null)
      .map(item => ({
        time: item.time,
        value: item.ema9!,
      }));

    const ema21Data = data
      .filter(item => item.ema21 != null)
      .map(item => ({
        time: item.time,
        value: item.ema21!,
      }));

    const ema200Data = data
      .filter(item => item.ema200 != null)
      .map(item => ({
        time: item.time,
        value: item.ema200!,
      }));

    // Define os dados nas séries
    candleSeries.setData(candleData);
    volumeSeries.setData(volumeData);
    
    if (ema9Data.length > 0) {
      ema9Series.setData(ema9Data);
    }
    
    if (ema21Data.length > 0) {
      ema21Series.setData(ema21Data);
    }
    
    if (ema200Data.length > 0) {
      ema200Series.setData(ema200Data);
    }

    // Ajusta o gráfico para mostrar todos os dados
    chart.timeScale().fitContent();

    // Handle resize
    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data]);

  if (data.length === 0) {
    return (
      <div className="bg-gray-800/50 rounded-xl p-8 border border-gray-700 text-center">
        <p className="text-gray-400">Nenhum dado de gráfico disponível</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-200">Gráfico de Candlestick - {symbol}</h3>
        <div className="flex items-center space-x-4 text-xs">
          <div className="flex items-center space-x-1">
            <div className="w-3 h-0.5 bg-blue-400"></div>
            <span className="text-gray-400">EMA 9</span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-3 h-0.5 bg-orange-400"></div>
            <span className="text-gray-400">EMA 21</span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-3 h-0.5 bg-purple-400"></div>
            <span className="text-gray-400">EMA 200</span>
          </div>
        </div>
      </div>
      <div ref={chartContainerRef} className="w-full" />
      <div className="mt-3 text-xs text-gray-500 text-center">
        Timeframe: 4h • Últimos 200 candles • Volume na parte inferior
      </div>
    </div>
  );
};

export default CandlestickChart;
