"""Testes da Semana 3 — Programação funcional. NÃO ALTERE ESTE ARQUIVO."""

import ast
import inspect
from pathlib import Path

import pytest

import funcional
from funcional import (
    ALIQUOTA_PADRAO,
    ALIQUOTAS,
    Item,
    aliquota,
    economia_total,
    filtrar_por_categoria,
    imposto_item,
    ordenar_por_preco,
    total_compra,
    total_impostos,
)

ARQUIVO = Path(funcional.__file__)


def _arvore_do_modulo():
    return ast.parse(ARQUIVO.read_text(encoding="utf-8"))


def _chamadas_na_funcao(funcao):
    """Nomes das funções chamadas dentro de uma função (ex.: {'map', 'sum'})."""
    arvore = ast.parse(inspect.getsource(funcao))
    return {
        no.func.id
        for no in ast.walk(arvore)
        if isinstance(no, ast.Call) and isinstance(no.func, ast.Name)
    }


def _tem_lambda(funcao):
    arvore = ast.parse(inspect.getsource(funcao))
    return any(isinstance(no, ast.Lambda) for no in ast.walk(arvore))


@pytest.fixture
def itens():
    return [
        Item("Feijão 1kg", 8.00, "cesta_basica", 2),
        Item("Iogurte", 7.50, "reduzido", 1),
        Item("Chocolate", 10.00, "padrao", 1),
        Item("Arroz 5kg", 26.00, "cesta_basica", 1),
    ]


# ---------- Regras do paradigma ----------

def test_nao_usa_class():
    classes = [n for n in ast.walk(_arvore_do_modulo()) if isinstance(n, ast.ClassDef)]
    assert classes == [], "funcional.py não deve definir classes"


def test_nao_usa_lacos_for_ou_while():
    lacos = [
        n for n in ast.walk(_arvore_do_modulo()) if isinstance(n, (ast.For, ast.While))
    ]
    assert lacos == [], "use map/filter/sorted/compreensões em vez de for/while"


def test_total_impostos_usa_map():
    assert "map" in _chamadas_na_funcao(total_impostos)


def test_filtrar_usa_filter():
    assert "filter" in _chamadas_na_funcao(filtrar_por_categoria)


def test_ordenar_usa_sorted_com_lambda():
    assert "sorted" in _chamadas_na_funcao(ordenar_por_preco)
    assert _tem_lambda(ordenar_por_preco)


# ---------- Dados ----------

def test_constantes():
    assert ALIQUOTA_PADRAO == pytest.approx(0.25)
    assert ALIQUOTAS == pytest.approx(
        {"cesta_basica": 0.0, "reduzido": 0.10, "padrao": 0.25}
    )


def test_item_e_namedtuple_imutavel():
    item = Item("Café 500g", 18.0, "cesta_basica", 2)
    assert item.nome == "Café 500g" and item.quantidade == 2
    with pytest.raises(AttributeError):
        item.preco = 1.0


def test_item_quantidade_padrao_e_1():
    assert Item("Café 500g", 18.0, "cesta_basica").quantidade == 1


# ---------- aliquota / imposto_item ----------

@pytest.mark.parametrize(
    "categoria, esperado",
    [("cesta_basica", 0.0), ("reduzido", 0.10), ("padrao", 0.25)],
)
def test_aliquota(categoria, esperado):
    assert aliquota(categoria) == pytest.approx(esperado)


def test_aliquota_categoria_invalida_lanca_value_error():
    with pytest.raises(ValueError):
        aliquota("luxo")


def test_imposto_item_cesta_basica_e_zero():
    assert imposto_item(Item("Arroz", 25.90, "cesta_basica", 3)) == pytest.approx(0.0)


def test_imposto_item_considera_quantidade():
    assert imposto_item(Item("Chocolate", 10.0, "padrao", 3)) == pytest.approx(7.50)


def test_imposto_item_calcula_por_unidade():
    # round(3.33 * 0.25, 2) = 0.83 -> 3 x 0.83 = 2.49
    assert imposto_item(Item("Bala", 3.33, "padrao", 3)) == pytest.approx(2.49)


# ---------- Totais ----------

def test_total_impostos(itens):
    assert total_impostos(itens) == pytest.approx(3.25)


def test_total_compra(itens):
    # subtotal 59.50 + impostos 3.25
    assert total_compra(itens) == pytest.approx(62.75)


def test_totais_lista_vazia():
    assert total_impostos([]) == pytest.approx(0.0)
    assert total_compra([]) == pytest.approx(0.0)
    assert economia_total([]) == pytest.approx(0.0)


def test_economia_total(itens):
    # se tudo fosse padrão: 4.00 + 1.88 + 2.50 + 6.50 = 14.88 ; cobrado 3.25
    assert economia_total(itens) == pytest.approx(11.63)


def test_mesmos_resultados_que_a_versao_oo():
    """Os dois paradigmas devem chegar ao mesmo número (exemplo do enunciado)."""
    itens = [Item("Feijão 1kg", 8.00, "cesta_basica", 2), Item("Chocolate", 10.00, "padrao")]
    assert total_impostos(itens) == pytest.approx(2.50)
    assert economia_total(itens) == pytest.approx(4.00)


# ---------- filtrar / ordenar ----------

def test_filtrar_por_categoria(itens):
    resultado = filtrar_por_categoria(itens, "cesta_basica")
    assert isinstance(resultado, list)
    assert [i.nome for i in resultado] == ["Feijão 1kg", "Arroz 5kg"]


def test_filtrar_categoria_sem_itens(itens):
    assert filtrar_por_categoria(itens, "inexistente") == []


def test_ordenar_crescente(itens):
    resultado = ordenar_por_preco(itens)
    assert isinstance(resultado, list)
    assert [i.preco for i in resultado] == [7.50, 8.00, 10.00, 26.00]


def test_ordenar_decrescente(itens):
    resultado = ordenar_por_preco(itens, decrescente=True)
    assert [i.preco for i in resultado] == [26.00, 10.00, 8.00, 7.50]


# ---------- Imutabilidade / pureza ----------

def test_funcoes_nao_alteram_a_lista_recebida(itens):
    copia = list(itens)
    total_impostos(itens)
    total_compra(itens)
    economia_total(itens)
    filtrar_por_categoria(itens, "padrao")
    ordenar_por_preco(itens, decrescente=True)
    assert itens == copia


def test_ordenar_retorna_lista_nova(itens):
    assert ordenar_por_preco(itens) is not itens


def test_funcoes_aceitam_tupla(itens):
    tupla = tuple(itens)
    assert total_compra(tupla) == pytest.approx(62.75)
    assert len(filtrar_por_categoria(tupla, "padrao")) == 1


def test_funcao_pura_mesma_entrada_mesma_saida(itens):
    assert total_compra(itens) == total_compra(itens)
