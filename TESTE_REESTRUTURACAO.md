# 🧪 Guia de Teste - Nova Estrutura do Frontend

## 🚀 Como Testar as Mudanças

### 1️⃣ Iniciar o Frontend

```bash
cd frontend
npm run dev
```

Acesse: `http://localhost:3000`

---

## 📋 Roteiro de Testes

### ✅ Teste 1: Tela Inicial
**O que verificar:**
- [ ] Logo e título aparecem centralizados
- [ ] 3 cards de seleção (BTC, ETH, SOL) visíveis
- [ ] Hover nos cards mostra animação de scale
- [ ] Botão "Comparar Ativos" está visível
- [ ] Footer com disclaimer está no final

**Como testar:**
1. Abra a aplicação
2. Observe o layout inicial
3. Passe o mouse sobre os cards
4. Verifique responsividade redimensionando a janela

---

### ✅ Teste 2: Modo Individual

**O que verificar:**
- [ ] Ao clicar em BTC, abre apenas a análise do Bitcoin
- [ ] Botão "Voltar" aparece no topo
- [ ] Card ocupa máximo de 800px centralizado
- [ ] Nenhum texto ultrapassa os limites do card
- [ ] Botão "Analisar agora" funciona corretamente

**Como testar:**
1. Na tela inicial, clique em **BTC**
2. Observe se apenas o Bitcoin aparece
3. Clique em "Analisar agora"
4. Verifique se todos os textos estão dentro dos limites
5. Role a página e verifique overflow
6. Clique em "Voltar"
7. Repita com **ETH** e **SOL**

**Seções a verificar:**
- Score de Análise
- Análise da IA
- Trade Rápido
- Gráfico de Candlestick
- Diagnóstico Técnico
- Indicadores Técnicos (Tendência, Momentum, Volatilidade, Volume, Força)

---

### ✅ Teste 3: Modo Comparação

**O que verificar:**
- [ ] Botão "Comparar Ativos" muda de cor ao clicar
- [ ] Seleção de até 2 ativos funciona
- [ ] Badge "✓ Selecionado" aparece nos cards escolhidos
- [ ] Contador mostra "X/2 selecionados"
- [ ] Botão "Comparar [ATIVO1] vs [ATIVO2]" aparece
- [ ] Ao confirmar, mostra 2 análises lado a lado

**Como testar:**
1. Na tela inicial, clique em **"Comparar Ativos"**
2. O botão deve ficar roxo/rosa
3. Clique em **ETH** (deve aparecer badge "Selecionado")
4. Clique em **SOL** (deve aparecer badge "Selecionado")
5. Tente clicar em **BTC** (não deve selecionar, limite de 2)
6. Clique em "Comparar ETH vs SOL"
7. Verifique layout lado a lado em desktop
8. Redimensione para mobile e veja stack vertical
9. Clique em "Voltar"

---

### ✅ Teste 4: Responsividade

**Breakpoints a testar:**

#### 📱 Mobile (< 640px)
- [ ] 1 coluna em todos os grids
- [ ] Cards de seleção empilhados
- [ ] Comparação empilhada verticalmente
- [ ] Textos se ajustam sem overflow
- [ ] Header do gráfico quebra em 2 linhas

#### 📱 Tablet (640px - 1024px)
- [ ] 2 colunas nos indicadores
- [ ] Cards de seleção em 3 colunas
- [ ] Comparação em 2 colunas
- [ ] Espaçamentos adequados

#### 💻 Desktop (> 1024px)
- [ ] 3 colunas nos indicadores principais
- [ ] 4 colunas na volatilidade
- [ ] Layout completo lado a lado na comparação
- [ ] Centralização com max-width

**Como testar:**
1. Abra DevTools (F12)
2. Ative o modo responsivo (Ctrl+Shift+M)
3. Teste resoluções: 375px, 768px, 1024px, 1440px
4. Verifique cada tela em cada resolução

---

### ✅ Teste 5: Overflow de Texto

**Casos específicos a verificar:**

#### 1. Análise da IA
- [ ] Comentário longo quebra corretamente
- [ ] Não ultrapassa bordas do card
- [ ] Ícone 🤖 não desalinha

#### 2. Diagnóstico Técnico
- [ ] Texto longo quebra em múltiplas linhas
- [ ] Não causa overflow horizontal

#### 3. Trade Rápido
- [ ] Comentário quebra corretamente
- [ ] Percentual não desalinha
- [ ] Labels ficam dentro do card

#### 4. Indicadores
- [ ] Nomes longos quebram
- [ ] Valores numéricos truncam se muito longos
- [ ] Descrições quebram em múltiplas linhas
- [ ] Badge "★ Importante" não quebra linha

#### 5. Gráfico
- [ ] Legendas das EMAs não ultrapassam
- [ ] Título trunca se necessário
- [ ] Gráfico redimensiona corretamente

**Como testar:**
1. Analise cada ativo
2. Reduza a largura da tela gradualmente
3. Observe se algum texto ultrapassa
4. Verifique scroll horizontal (não deve existir)

---

### ✅ Teste 6: Navegação

**Fluxo completo:**
```
Home → BTC (Single) → Voltar → 
Home → Comparar → Selecionar ETH e SOL → Comparar → Voltar → 
Home → SOL (Single) → Voltar → Home
```

**O que verificar:**
- [ ] Transições suaves entre telas
- [ ] Estado limpo ao voltar (não mantém seleções antigas)
- [ ] Botão "Voltar" sempre visível quando necessário
- [ ] Modo comparação desativa ao voltar

---

### ✅ Teste 7: Funcionalidade da API

**Com Backend Rodando:**

1. Inicie o backend:
```bash
python run.py
```

2. No frontend, teste:
- [ ] Análise carrega dados reais da API
- [ ] Loading aparece durante carregamento
- [ ] Dados são exibidos corretamente
- [ ] Erros são tratados e exibidos

**Sem Backend:**
- [ ] Mensagem de erro clara aparece
- [ ] Interface não quebra
- [ ] Possível voltar e tentar outro ativo

---

## 🐛 Problemas Conhecidos (Se Houver)

### Antes de Reportar um Bug:

1. Limpe o cache do navegador (Ctrl+Shift+Del)
2. Force reload (Ctrl+F5)
3. Verifique se o backend está rodando (se testando com API)
4. Verifique console do navegador (F12) para erros
5. Teste em modo anônimo

---

## 📊 Checklist de Qualidade Visual

### Desktop
- [ ] Análise individual centralizada (800px max)
- [ ] Comparação ocupa largura apropriada
- [ ] Cards de seleção bem espaçados
- [ ] Animações suaves
- [ ] Sem overflow horizontal
- [ ] Textos legíveis

### Mobile
- [ ] Tudo empilhado verticalmente
- [ ] Cards de seleção em tela cheia
- [ ] Botões grandes o suficiente para toque
- [ ] Textos legíveis sem zoom
- [ ] Scroll suave
- [ ] Sem elementos cortados

### Tablet
- [ ] Layout intermediário funciona
- [ ] 2 colunas onde apropriado
- [ ] Espaçamentos adequados
- [ ] Transições suaves entre breakpoints

---

## 🎨 Verificação de Design

### Cores
- [ ] Dark mode consistente
- [ ] Verde para sinais positivos
- [ ] Vermelho para sinais negativos
- [ ] Amarelo para neutro
- [ ] Roxo/Rosa para modo comparação
- [ ] Azul para interações

### Tipografia
- [ ] Hierarquia clara de títulos
- [ ] Textos legíveis
- [ ] Tamanhos responsivos
- [ ] Peso (weight) apropriado

### Espaçamento
- [ ] Padding consistente
- [ ] Gaps apropriados
- [ ] Margens balanceadas
- [ ] Breathing room entre seções

### Interação
- [ ] Hover states visíveis
- [ ] Botões com feedback
- [ ] Animações não exageradas
- [ ] Focus visible (Tab navigation)

---

## 📸 Screenshots Sugeridos

Para documentação, tire screenshots de:

1. **Tela Inicial**
   - Desktop
   - Mobile

2. **Análise Individual**
   - Bitcoin completo
   - Ethereum completo
   - Solana completo

3. **Modo Comparação**
   - Seleção de ativos
   - Comparação lado a lado (desktop)
   - Comparação empilhada (mobile)

4. **Detalhes**
   - Score colorido
   - Trade Rápido
   - Gráfico de Candlestick
   - Grid de indicadores

---

## 🔧 Resolução de Problemas

### Problema: Textos ainda ultrapassam
**Solução:**
1. Verifique se os arquivos foram salvos
2. Force reload (Ctrl+F5)
3. Limpe cache do Next.js: `rm -rf .next`
4. Reinicie o dev server

### Problema: Comparação não funciona
**Solução:**
1. Verifique console (F12)
2. Confirme que selecionou exatamente 2 ativos
3. Recarregue a página

### Problema: Layout quebrado
**Solução:**
1. Verifique se todas as dependências estão instaladas
2. Execute `npm install` novamente
3. Reinicie o servidor

### Problema: API não carrega
**Solução:**
1. Verifique se backend está rodando
2. Confirme URL em `frontend/lib/api.ts`
3. Verifique CORS no backend
4. Veja erros no console

---

## ✅ Aprovação Final

Antes de considerar concluído, verifique:

- [ ] Todos os testes acima passaram
- [ ] Nenhum erro no console
- [ ] Nenhum warning de lint
- [ ] TypeScript sem erros
- [ ] Build production funciona: `npm run build`
- [ ] Performance aceitável
- [ ] Responsividade em todos os breakpoints
- [ ] Textos dentro dos limites em todos os cenários

---

## 🎉 Resultado Esperado

Após todos os testes, você deve ter:

✅ Interface moderna e limpa  
✅ Navegação intuitiva entre telas  
✅ Modo individual focado (1 ativo)  
✅ Modo comparação funcional (2 ativos)  
✅ Nenhum overflow de texto  
✅ Design responsivo perfeito  
✅ Experiência de usuário superior  

---

**Happy Testing! 🚀**

