# Trabalho Prático — Calculadora de Impostos da Cesta Básica

**Disciplina:** Paradigmas de Programação
**Duração:** 4 semanas (um módulo por semana)
**Linguagem:** Python 3.10 ou superior
**Correção:** automática, com `pytest`

---

## 1. Contexto: o novo imposto sobre o consumo

### 1.1 O que mudou

A Reforma Tributária (Emenda Constitucional nº 132/2023, regulamentada pela Lei Complementar nº 214/2025) substitui cinco tributos sobre o consumo por um modelo chamado **IVA dual** (Imposto sobre Valor Agregado), formado por dois tributos:

| Novo tributo | Quem arrecada | O que substitui |
|---|---|---|
| **CBS** — Contribuição sobre Bens e Serviços | União (federal) | PIS e Cofins |
| **IBS** — Imposto sobre Bens e Serviços | Estados e municípios | ICMS (estadual) e ISS (municipal) |

Além deles, foi criado o **Imposto Seletivo**, que incide sobre produtos prejudiciais à saúde ou ao meio ambiente (como cigarros e bebidas alcoólicas). Ele não faz parte deste trabalho.

Três características do IBS/CBS importam para o nosso sistema:

1. **Cobrança "por fora":** o imposto é calculado sobre o preço do produto *sem* imposto e somado a ele. Por isso, no trabalho, `preço final = preço + preço × alíquota`.
2. **Não cumulatividade:** em cada etapa da cadeia (produtor → indústria → atacado → supermercado), a empresa paga imposto apenas sobre o valor que ela agregou. Ela faz isso descontando, como **crédito**, o imposto que já foi pago nas etapas anteriores.
3. **Transição gradual:** em 2026 o imposto aparece na nota fiscal com alíquotas de teste (0,9% de CBS e 0,1% de IBS). A CBS passa a ser cobrada de verdade em 2027, e o IBS cresce gradualmente entre 2029 e 2032, até substituir totalmente ICMS e ISS em 2033.

### 1.2 A Cesta Básica Nacional

A reforma criou a **Cesta Básica Nacional de Alimentos**. Os alimentos dessa lista (Anexo I da LC 214/2025 — arroz, feijão, leite, carnes, café, pão francês, entre outros), além de frutas, hortaliças e ovos (Anexo XV), têm **alíquota zero** de IBS e CBS.

Outros alimentos não chegam a zero, mas têm **redução de 60%** da alíquota (Anexo VII), ou seja, pagam apenas 40% da alíquota padrão. Os demais produtos pagam a alíquota padrão.

### 1.3 Alíquota zero não é a mesma coisa que isenção

No dia a dia, as notícias falam em "isenção da cesta básica". Juridicamente, porém, são mecanismos diferentes:

| | **Isenção** | **Alíquota zero** |
|---|---|---|
| O que é | A lei **dispensa o pagamento** de um imposto que seria devido | O imposto **existe e é calculado**, mas a alíquota é 0%, e o resultado é zero |
| O cálculo acontece? | Não — a operação é retirada da cobrança | Sim — base × 0% = R$ 0,00 |
| Créditos das etapas anteriores | Em regra, **são anulados**: o imposto pago pelo fornecedor vira custo da empresa | **São mantidos**: a empresa continua aproveitando o crédito do que pagou antes |
| Efeito no preço | Parte do imposto "escondido" nas etapas anteriores continua embutida no preço | O benefício chega de forma mais completa ao consumidor |

**Exemplo:** um supermercado compra arroz de um fornecedor que pagou imposto sobre embalagens e transporte.
- Com **isenção**, o supermercado perderia o crédito desse imposto anterior, que viraria custo e poderia ser repassado ao preço.
- Com **alíquota zero**, o supermercado não cobra imposto do consumidor *e* mantém o crédito. Por isso o legislador escolheu alíquota zero para a cesta básica.

**Ligação com o código:** no nosso sistema, um produto da cesta básica **não pula o cálculo**. O método `imposto()` é executado normalmente e retorna `0.0`, porque a alíquota é zero. É exatamente isso que significa "alíquota zero" — e é também um bom exemplo de **polimorfismo**: todos os produtos respondem ao mesmo método, cada um com sua regra.

### 1.4 Simplificações adotadas no trabalho

- A alíquota padrão real ainda será definida. Usaremos uma **alíquota padrão hipotética de 25%** (constante `ALIQUOTA_PADRAO = 0.25`).
- Não usaremos códigos NCM: a categoria do produto é informada diretamente.
- Não trataremos créditos entre empresas, cashback nem Imposto Seletivo.

| Categoria | Exemplos | Alíquota efetiva |
|---|---|---|
| Cesta básica | arroz, feijão, leite, café, ovos | 0% |
| Alimento com redução | (lista simplificada do Anexo VII) | 10% (40% de 25%) |
| Padrão | refrigerante, chocolate, biscoito recheado | 25% |

---

## 2. Objetivo

Construir um sistema que calcula os impostos de uma compra de supermercado e mostra quanto o consumidor economizou com a desoneração. O mesmo problema será resolvido primeiro com **orientação a objetos** (semanas 1 e 2) e depois com **programação funcional** (semanas 3 e 4).

**Regra de arredondamento (todas as semanas):** todo valor monetário retornado é arredondado com `round(valor, 2)`. O imposto é calculado **por unidade**, arredondado, e depois multiplicado pela quantidade.

---

## 3. Semana 1 — Modelando produtos

**Conceitos:** classes, encapsulamento, herança, polimorfismo.
**Arquivo:** `produtos.py` (template fornecido)

- Constante `ALIQUOTA_PADRAO = 0.25`.
- Classe base `Produto(nome, preco)`:
  - `preco` é uma `@property`. O valor não pode ser negativo, nem na criação nem em alterações posteriores (lançar `ValueError`).
  - `aliquota()` na classe base lança `NotImplementedError`.
  - `imposto()` → `round(preco × aliquota(), 2)`.
  - `preco_final()` → `round(preco + imposto(), 2)`.
  - `__str__` → `Arroz 5kg - R$ 25.90 (imposto: R$ 0.00)`.
- Subclasses que sobrescrevem `aliquota()`:
  - `ProdutoCestaBasica` → `0.0`
  - `ProdutoReduzido` → 40% de `ALIQUOTA_PADRAO` (0.10)
  - `ProdutoPadrao` → `ALIQUOTA_PADRAO` (0.25)

```python
>>> arroz = ProdutoCestaBasica("Arroz 5kg", 25.90)
>>> refri = ProdutoPadrao("Refrigerante 2L", 9.00)
>>> refri.imposto()
2.25
>>> print(arroz)
Arroz 5kg - R$ 25.90 (imposto: R$ 0.00)
```

**Testes:** `pytest tests/test_semana1.py -v`

---

## 4. Semana 2 — O carrinho de compras

**Conceitos:** composição, métodos especiais (*dunder methods*), tratamento de erros.
**Arquivo:** `carrinho.py` (template fornecido)

Classe `Carrinho`, que guarda produtos e suas quantidades:

- `adicionar(produto, quantidade=1)`:
  - `produto` deve ser instância de `Produto` (senão, `TypeError`);
  - `quantidade` deve ser inteiro ≥ 1 (senão, `ValueError`);
  - adicionar um produto com o mesmo nome **soma** a quantidade.
- `remover(nome)` → remove o produto inteiro; lança `KeyError` se não existir.
- `subtotal()` → soma de `preço × quantidade` (sem impostos).
- `total_impostos()` → soma de `imposto() × quantidade`.
- `total()` → `subtotal() + total_impostos()`.
- `economia()` → quanto o consumidor pagaria **a mais** se todos os produtos tivessem a alíquota padrão:
  `soma de round(preço × ALIQUOTA_PADRAO, 2) × quantidade` − `total_impostos()`.
- `__len__` → total de **unidades** no carrinho.
- `__contains__` → permite `"Arroz 5kg" in carrinho`.

```python
>>> c = Carrinho()
>>> c.adicionar(ProdutoCestaBasica("Feijão 1kg", 8.00), 2)
>>> c.adicionar(ProdutoPadrao("Chocolate", 10.00))
>>> c.total_impostos()
2.5
>>> c.economia()   # 2 x 2.00 do feijão que não foram cobrados
4.0
>>> len(c)
3
```

**Testes:** `pytest tests/test_semana2.py -v`

---

## 5. Semana 3 — Reescrevendo com programação funcional

**Conceitos:** funções puras, imutabilidade, `map`, `filter`, `sorted`, `lambda`.
**Arquivo:** `funcional.py` (**criado por você**, sem template)

Regras do paradigma, **verificadas pelos testes**:
- não usar `class` (exceto a `namedtuple` abaixo);
- não usar laços `for` ou `while` (compreensões de lista são permitidas);
- não alterar a lista recebida como parâmetro.

Definir:
- `ALIQUOTA_PADRAO = 0.25`
- `ALIQUOTAS = {"cesta_basica": 0.0, "reduzido": 0.10, "padrao": 0.25}`
- `Item = namedtuple("Item", ["nome", "preco", "categoria", "quantidade"], defaults=[1])`

Funções:
| Função | O que faz | Exigência |
|---|---|---|
| `aliquota(categoria)` | retorna a alíquota; `ValueError` se a categoria não existir | — |
| `imposto_item(item)` | `round(round(preco × alíquota, 2) × quantidade, 2)` | — |
| `total_impostos(itens)` | soma dos impostos de todos os itens | usar `map` |
| `total_compra(itens)` | soma de `preço × quantidade` + impostos | — |
| `filtrar_por_categoria(itens, categoria)` | lista apenas os itens da categoria | usar `filter` |
| `ordenar_por_preco(itens, decrescente=False)` | nova lista ordenada pelo preço unitário | usar `sorted` com `lambda` |
| `economia_total(itens)` | mesma regra da semana 2 | — |

As funções que retornam itens devem retornar uma **lista nova**.

**Testes:** `pytest tests/test_semana3.py -v`

---

## 6. Semana 4 — Funções de ordem superior e relatório final

**Conceitos:** *closures*, composição de funções, funções que retornam funções.
**Arquivo:** `funcional.py` (continuação; as mesmas regras da semana 3 valem aqui)

- `criar_calculadora(aliquota_padrao)` → retorna uma **função** `calcular(item)` que calcula o imposto do item usando outra alíquota padrão (cesta básica = 0; reduzido = 40% da padrão; padrão = a própria). Lança `ValueError` se `aliquota_padrao` for negativa.
  ```python
  >>> calc27 = criar_calculadora(0.27)
  >>> calc27(Item("Chocolate", 10.00, "padrao"))
  2.7
  ```
- `compor(*funcoes)` → retorna uma função que aplica as funções **da direita para a esquerda**: `compor(f, g)(x) == f(g(x))`. Sem funções, retorna a identidade.
- `gerar_relatorio(itens)` → retorna um dicionário:
  ```python
  {
      "por_categoria": {"cesta_basica": ..., "reduzido": ..., "padrao": ...},  # valor final (com imposto) por categoria
      "total_impostos": ...,
      "total": ...,
      "economia": ...,
  }
  ```
  As três categorias devem aparecer sempre, mesmo com valor `0.0`.

**Entrega final:** preencher o arquivo `RESPOSTAS.md` (até 1 página).

**Testes:** `pytest tests/test_semana4.py -v`

---

## 7. Como trabalhar e entregar

1. Aceite o repositório da atividade no GitHub e clone-o.
2. Instale o pytest: `pip install -r requirements.txt`
3. Rode os testes da semana: `pytest tests/test_semana1.py -v`
4. Faça *commit* e *push* a cada semana. O GitHub Actions roda os testes automaticamente e mostra o resultado de cada semana separadamente na aba **Actions**.

**Importante:**
- Os nomes de arquivos, classes, funções e constantes devem ser **exatamente** os do enunciado.
- **Não altere** a pasta `tests/` nem o arquivo `.github/workflows/testes.yml`.
- Durante as semanas 1 e 2 é normal os testes das semanas 3 e 4 falharem (o `funcional.py` ainda não existe).

---

## 8. Avaliação

| Item | Peso |
|---|---|
| Testes da semana 1 | 20% |
| Testes da semana 2 | 25% |
| Testes da semana 3 | 25% |
| Testes da semana 4 | 20% |
| `RESPOSTAS.md` | 10% |

A nota de cada semana é proporcional à quantidade de testes aprovados.

---

## 9. Referências

- Emenda Constitucional nº 132/2023 — art. 8º (Cesta Básica Nacional de Alimentos) e art. 156-A da Constituição Federal (IBS).
- Lei Complementar nº 214/2025 — art. 125 e Anexo I (cesta básica com alíquota zero); Anexo XV (hortícolas, frutas e ovos); art. 135 e Anexo VII (alimentos com redução de 60%).
