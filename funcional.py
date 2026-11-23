"""
Semana 3 — Reescrevendo com programação funcional

Conceitos: funções puras, imutabilidade, map, filter, sorted e lambda.
Regras: sem classes (exceto a namedtuple), sem laços for/while
e sem alterar a lista recebida como parâmetro.
"""

from collections import namedtuple

ALIQUOTA_PADRAO = 0.25  # alíquota padrão hipotética (IBS + CBS)

ALIQUOTAS = {
    "cesta_basica": 0.0,
    "reduzido": 0.4 * ALIQUOTA_PADRAO,  # redução de 60% -> 0.10
    "padrao": ALIQUOTA_PADRAO,
}

Item = namedtuple("Item", ["nome", "preco", "categoria", "quantidade"], defaults=[1])


def aliquota(categoria):
    """Retorna a alíquota da categoria; ValueError se ela não existir."""
    if categoria not in ALIQUOTAS:
        raise ValueError(f"Categoria desconhecida: {categoria!r}")
    return ALIQUOTAS[categoria]


def imposto_item(item):
    """Imposto do item: calculado por unidade, arredondado e multiplicado pela quantidade."""
    return round(round(item.preco * aliquota(item.categoria), 2) * item.quantidade, 2)


def total_impostos(itens):
    """Soma dos impostos de todos os itens."""
    return round(sum(map(imposto_item, itens)), 2)


def total_compra(itens):
    """Soma de preço × quantidade, mais os impostos."""
    subtotal = sum(item.preco * item.quantidade for item in itens)
    return round(subtotal + total_impostos(itens), 2)


def filtrar_por_categoria(itens, categoria):
    """Nova lista apenas com os itens da categoria informada."""
    return list(filter(lambda item: item.categoria == categoria, itens))


def ordenar_por_preco(itens, decrescente=False):
    """Nova lista ordenada pelo preço unitário."""
    return sorted(itens, key=lambda item: item.preco, reverse=decrescente)


def economia_total(itens):
    """Quanto o consumidor pagaria a mais se tudo tivesse a alíquota padrão."""
    imposto_se_padrao = sum(
        round(item.preco * ALIQUOTA_PADRAO, 2) * item.quantidade for item in itens
    )
    return round(imposto_se_padrao - total_impostos(itens), 2)


if __name__ == "__main__":
    compra = [
        Item("Feijão 1kg", 8.00, "cesta_basica", 2),
        Item("Chocolate", 10.00, "padrao"),
    ]
    print("Impostos:", total_impostos(compra))
    print("Total:", total_compra(compra))
    print("Economia:", economia_total(compra))
