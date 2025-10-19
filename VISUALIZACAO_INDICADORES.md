# 🎨 Visualização da Nova Interface de Indicadores

## 📊 Layout Completo

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  📊 Indicadores Técnicos                                          ┃
┃  Análise detalhada com descrições educacionais                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

╔═══════════════════════════════════════════════════════════════════╗
║ 📈 Tendência                                    Médias Móveis     ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ ║
║  │ EMA 9            │  │ EMA 21           │  │ EMA 50           │ ║
║  │ ★ Importante     │  │ ★ Importante     │  │                  │ ║
║  │                  │  │                  │  │                  │ ║
║  │ 43,250.50        │  │ 42,890.25        │  │ 42,100.75        │ ║
║  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤ ║
║  │ Média móvel      │  │ Média móvel de   │  │ Média móvel de   │ ║
║  │ exponencial de   │  │ médio prazo.     │  │ longo prazo.     │ ║
║  │ curto prazo.     │  │ Ajuda a confirmar│  │ Identifica       │ ║
║  │ Mostra direção   │  │ tendência.       │  │ tendência        │ ║
║  │ imediata.        │  │                  │  │ principal.       │ ║
║  └──────────────────┘  └──────────────────┘  └──────────────────┘ ║
║                                                                   ║
║  ┌──────────────────┐  ┌──────────────────┐                      ║
║  │ EMA 200          │  │ SMA 100          │                      ║
║  │                  │  │                  │                      ║
║  │ 40,500.00        │  │ 41,200.50        │                      ║
║  ├──────────────────┤  ├──────────────────┤                      ║
║  │ Média móvel de   │  │ Média móvel      │                      ║
║  │ longo prazo muito│  │ simples de 100   │                      ║
║  │ importante.      │  │ períodos.        │                      ║
║  └──────────────────┘  └──────────────────┘                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════╗
║ ⚡ Momentum                                  Força do Movimento   ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ ║
║  │ RSI (14)         │  │ MACD             │  │ MACD Signal      │ ║
║  │ ★ Importante     │  │ ★ Importante     │  │                  │ ║
║  │                  │  │                  │  │                  │ ║
║  │ 75.32            │  │ -125.45          │  │ -98.20           │ ║
║  │ 🔴 Sobrecomprado │  │                  │  │                  │ ║
║  │ (Possível venda) │  │                  │  │                  │ ║
║  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤ ║
║  │ Mede a força do  │  │ Mostra           │  │ Linha de sinal   │ ║
║  │ movimento. Abaixo│  │ convergência/    │  │ do MACD. Média   │ ║
║  │ de 30 =          │  │ divergência de   │  │ móvel do MACD.   │ ║
║  │ sobrevendido;    │  │ médias móveis.   │  │                  │ ║
║  │ acima de 70 =    │  │                  │  │                  │ ║
║  │ sobrecomprado.   │  │                  │  │                  │ ║
║  └──────────────────┘  └──────────────────┘  └──────────────────┘ ║
║                                                                   ║
║  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ ║
║  │ MACD Histograma  │  │ Stoch RSI K      │  │ Stoch RSI D      │ ║
║  │                  │  │                  │  │                  │ ║
║  │ -27.25           │  │ 85.60            │  │ 82.30            │ ║
║  │                  │  │ 🔴 Sobrecomprado │  │                  │ ║
║  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤ ║
║  │ Diferença entre  │  │ Versão mais      │  │ Média móvel do   │ ║
║  │ MACD e Signal.   │  │ sensível do RSI. │  │ Stochastic RSI K.│ ║
║  │ Mostra força do  │  │ Oscila entre     │  │ Linha de sinal.  │ ║
║  │ momentum.        │  │ 0 e 100.         │  │                  │ ║
║  └──────────────────┘  └──────────────────┘  └──────────────────┘ ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════╗
║ ⚠️ Volatilidade                              Risco e Variação     ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  ║
║  │ ATR (14)   │  │ Bollinger  │  │ Bollinger  │  │ Bollinger  │  ║
║  │            │  │ Superior   │  │ Média      │  │ Inferior   │  ║
║  │ 1,245.80   │  │ 44,500.00  │  │ 42,000.00  │  │ 39,500.00  │  ║
║  ├────────────┤  ├────────────┤  ├────────────┤  ├────────────┤  ║
║  │ Average    │  │ Banda      │  │ Banda média│  │ Banda      │  ║
║  │ True Range.│  │ superior   │  │ (SMA 20) das│  │ inferior   │  ║
║  │ Mede       │  │ das        │  │ Bollinger  │  │ das        │  ║
║  │ volatilid. │  │ Bollinger. │  │ Bands.     │  │ Bollinger. │  ║
║  └────────────┘  └────────────┘  └────────────┘  └────────────┘  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

╔════════════════════════════════╗  ╔═══════════════════════════════╗
║ 📊 Volume         Liquidez     ║  ║ 🎯 Força        Intensidade   ║
╠════════════════════════════════╣  ╠═══════════════════════════════╣
║                                ║  ║                               ║
║  ┌──────────────────────────┐  ║  ║  ┌─────────────────────────┐  ║
║  │ Volume MA                │  ║  ║  │ ADX (14)                │  ║
║  │                          │  ║  ║  │                         │  ║
║  │ 25,430,000,000           │  ║  ║  │ 45.25                   │  ║
║  ├──────────────────────────┤  ║  ║  │ 🟡 Tendência forte      │  ║
║  │ Média móvel do volume.   │  ║  ║  ├─────────────────────────┤  ║
║  │ Compara volume atual com │  ║  ║  │ Mede a força da         │  ║
║  │ histórico.               │  ║  ║  │ tendência. Acima de     │  ║
║  └──────────────────────────┘  ║  ║  │ 25 = tendência forte.   │  ║
║                                ║  ║  └─────────────────────────┘  ║
║  ┌──────────────────────────┐  ║  ║                               ║
║  │ MFI (14)                 │  ║  ║  ┌─────────────────────────┐  ║
║  │                          │  ║  ║  │ Preço Atual             │  ║
║  │ 68.50                    │  ║  ║  │                         │  ║
║  │ 🟡 Neutro                │  ║  ║  │ 43,250.50               │  ║
║  ├──────────────────────────┤  ║  ║  ├─────────────────────────┤  ║
║  │ Combina preço e volume.  │  ║  ║  │ Último preço de         │  ║
║  │ Acima de 80 =            │  ║  ║  │ fechamento do ativo.    │  ║
║  │ sobrecomprado; abaixo de │  ║  ║  └─────────────────────────┘  ║
║  │ 20 = sobrevendido.       │  ║  ║                               ║
║  └──────────────────────────┘  ║  ║  ┌─────────────────────────┐  ║
║                                ║  ║  │ Volume Atual            │  ║
║  ┌──────────────────────────┐  ║  ║  │                         │  ║
║  │ OBV                      │  ║  ║  │ 28,500,000,000          │  ║
║  │                          │  ║  ║  ├─────────────────────────┤  ║
║  │ 1,250,000,000            │  ║  ║  │ Volume negociado no     │  ║
║  ├──────────────────────────┤  ║  ║  │ último período.         │  ║
║  │ Mostra fluxo de volume.  │  ║  ║  └─────────────────────────┘  ║
║  │ OBV crescente = entrada  │  ║  ║                               ║
║  │ de capital.              │  ║  ║                               ║
║  └──────────────────────────┘  ║  ║                               ║
║                                ║  ║                               ║
╚════════════════════════════════╝  ╚═══════════════════════════════╝
```

## 🎨 Legenda de Cores

### Bordas das Categorias
- 🔵 **Azul** (`border-blue-500/30`) - Tendência
- 🟣 **Roxo** (`border-purple-500/30`) - Momentum
- 🟡 **Amarelo** (`border-yellow-500/30`) - Volatilidade
- 🟢 **Verde** (`border-green-500/30`) - Volume
- 🟠 **Laranja** (`border-orange-500/30`) - Força

### Indicadores Importantes
- ⭐ **Badge Azul** - Marca indicadores-chave
- 🌟 **Glow Azul** - Sombra brilhante ao redor
- 💎 **Gradiente** - Background azul-roxo

### Interpretações
- 🟢 **Verde** - Sobrevendido / Compra
- 🔴 **Vermelho** - Sobrecomprado / Venda
- 🟡 **Amarelo** - Neutro / Normal

## 📱 Responsividade

### Desktop (> 1024px)
```
┌────────┬────────┬────────┐
│ Card 1 │ Card 2 │ Card 3 │
├────────┼────────┼────────┤
│ Card 4 │ Card 5 │        │
└────────┴────────┴────────┘
```

### Tablet (640px - 1024px)
```
┌────────┬────────┐
│ Card 1 │ Card 2 │
├────────┼────────┤
│ Card 3 │ Card 4 │
├────────┼────────┤
│ Card 5 │        │
└────────┴────────┘
```

### Mobile (< 640px)
```
┌────────┐
│ Card 1 │
├────────┤
│ Card 2 │
├────────┤
│ Card 3 │
├────────┤
│ Card 4 │
├────────┤
│ Card 5 │
└────────┘
```

## 🔍 Detalhes de um Card Importante

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  RSI (14)                            ★ Importante         ║  ← Badge azul
║  ─────────────────────────────────────────────────────    ║
║                                                           ║
║  75.32                                                    ║  ← Valor grande (2xl)
║                                                           ║
║  (Sobrecomprado - Possível venda)                         ║  ← Interpretação vermelha
║  ═════════════════════════════════════════════════════    ║  ← Divisor
║                                                           ║
║  Mede a força do movimento. Abaixo de 30 = sobrevendido  ║  ← Descrição
║  (barato); acima de 70 = sobrecomprado (caro).            ║     educacional
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
     ↑                                                    ↑
  Gradiente                                          Sombra com
  azul-roxo                                          glow azul
```

## 🔍 Detalhes de um Card Normal

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  EMA 50                                                 │  ← Sem badge
│  ───────────────────────────────────────────────────    │
│                                                         │
│  42,350.21                                              │  ← Valor grande
│                                                         │
│  ═══════════════════════════════════════════════════    │  ← Divisor
│                                                         │
│  Média móvel de longo prazo. Identifica tendência       │  ← Descrição
│  principal. Cruzamento com preço pode sinalizar         │     educacional
│  mudança de tendência.                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
     ↑
  Background
  cinza escuro
```

## 🎯 Hierarquia Visual

```
Nível 1: Título da Seção
  ┗━━━ 📊 Indicadores Técnicos

Nível 2: Categorias
  ┗━━━ 📈 Tendência | ⚡ Momentum | ⚠️ Volatilidade | 📊 Volume | 🎯 Força

Nível 3: Cards de Indicadores
  ┗━━━ ⭐ Importantes | 🔲 Normais

Nível 4: Conteúdo do Card
  ┗━━━ Nome > Valor > Interpretação > Descrição
```

## ✨ Efeitos Visuais

### Hover nos Cards
```
Normal:     scale(1.00)
Hover:      scale(1.02)
Transição:  duration-200
```

### Gradientes nos Indicadores Importantes
```
Background:  from-blue-900/40 to-purple-900/40
Border:      border-blue-500/50 (2px)
Shadow:      shadow-blue-500/20
```

### Cores de Interpretação
```javascript
// Verde (Compra/Sobrevendido)
text-green-400

// Vermelho (Venda/Sobrecomprado)
text-red-400

// Amarelo (Neutro)
text-yellow-400
```

## 📐 Espaçamentos

```
Seção Principal:    space-y-6
Grid de Cards:      gap-4
Padding Cards:      p-4
Padding Categorias: p-5
Margin Bottom:      mb-5
```

## 🎨 Tipografia

```
Título Seção:       text-xl font-bold
Título Categoria:   text-lg font-bold
Nome Indicador:     text-sm font-semibold
Valor:              text-2xl font-bold
Interpretação:      text-xs font-medium
Descrição:          text-xs (regular)
```

---

**Design System**: Tailwind CSS  
**Responsividade**: Mobile-first  
**Acessibilidade**: WCAG 2.1 AA  
**Performance**: Otimizado

