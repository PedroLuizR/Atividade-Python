"""Testes da Semana 4 — Ordem superior e relatório. NÃO ALTERE ESTE ARQUIVO."""

import ast
from pathlib import Path

import pytest

import funcional
from funcional import (
    Item,
    compor,
    criar_calculadora,
    economia_total,
    gerar_relatorio,
    total_compra,
    total_impostos,
)


@pytest.fixture
def itens():
    return [
        Item("Feijão 1kg", 8.00, "cesta_basica", 2),
        Item("Iogurte", 7.50, "reduzido", 1),
        Item("Chocolate", 10.00, "padrao", 1),
        Item("Arroz 5kg", 26.00, "cesta_basica", 1),
    ]


# ---------- Regra do paradigma (continua valendo) ----------

def test_continua_sem_for_while_e_sem_class():
    arvore = ast.parse(Path(funcional.__file__).read_text(encoding="utf-8"))
    proibidos = [
        n for n in ast.walk(arvore) if isinstance(n, (ast.For, ast.While, ast.ClassDef))
    ]
    assert proibidos == []


# ---------- criar_calculadora (closure) ----------

def test_criar_calculadora_retorna_funcao():
    assert callable(criar_calculadora(0.27))


def test_calculadora_e_uma_closure():
    calc = criar_calculadora(0.27)
    assert calc.__closure__ is not None, "a função retornada deve 'lembrar' a alíquota"


def test_calculadora_exemplo_do_enunciado():
    calc27 = criar_calculadora(0.27)
    assert calc27(Item("Chocolate", 10.00, "padrao")) == pytest.approx(2.70)


def test_calculadora_reduzido_usa_40_por_cento():
    calc30 = criar_calculadora(0.30)
    assert calc30(Item("Iogurte", 10.00, "reduzido")) == pytest.approx(1.20)


def test_calculadora_cesta_basica_sempre_zero():
    calc = criar_calculadora(0.50)
    assert calc(Item("Arroz", 25.90, "cesta_basica", 4)) == pytest.approx(0.0)


def test_calculadora_considera_quantidade():
    calc = criar_calculadora(0.20)
    assert calc(Item("Chocolate", 10.00, "padrao", 3)) == pytest.approx(6.00)


def test_calculadoras_sao_independentes():
    calc10 = criar_calculadora(0.10)
    calc40 = criar_calculadora(0.40)
    item = Item("Chocolate", 10.00, "padrao")
    assert calc10(item) == pytest.approx(1.00)
    assert calc40(item) == pytest.approx(4.00)


def test_calculadora_com_25_bate_com_semana3(itens):
    calc25 = criar_calculadora(0.25)
    assert sum(map(calc25, itens)) == pytest.approx(total_impostos(itens))


def test_calculadora_aliquota_negativa_lanca_value_error():
    with pytest.raises(ValueError):
        criar_calculadora(-0.1)


# ---------- compor ----------

def test_compor_direita_para_esquerda():
    dobro = lambda x: x * 2
    mais_um = lambda x: x + 1
    assert compor(dobro, mais_um)(5) == 12   # dobro(mais_um(5))
    assert compor(mais_um, dobro)(5) == 11   # mais_um(dobro(5))


def test_compor_tres_funcoes():
    f = compor(str, abs, lambda x: x - 10)
    assert f(3) == "7"


def test_compor_uma_funcao():
    assert compor(abs)(-4) == 4


def test_compor_sem_funcoes_e_identidade():
    assert compor()(42) == 42


def test_compor_com_funcoes_do_trabalho(itens):
    from funcional import filtrar_por_categoria

    impostos_do_padrao = compor(total_impostos, lambda xs: filtrar_por_categoria(xs, "padrao"))
    assert impostos_do_padrao(itens) == pytest.approx(2.50)


# ---------- gerar_relatorio ----------

def test_relatorio_tem_as_chaves(itens):
    rel = gerar_relatorio(itens)
    assert set(rel) == {"por_categoria", "total_impostos", "total", "economia"}
    assert set(rel["por_categoria"]) == {"cesta_basica", "reduzido", "padrao"}


def test_relatorio_por_categoria(itens):
    por_cat = gerar_relatorio(itens)["por_categoria"]
    assert por_cat["cesta_basica"] == pytest.approx(42.00)   # 16.00 + 26.00
    assert por_cat["reduzido"] == pytest.approx(8.25)
    assert por_cat["padrao"] == pytest.approx(12.50)


def test_relatorio_totais(itens):
    rel = gerar_relatorio(itens)
    assert rel["total_impostos"] == pytest.approx(3.25)
    assert rel["total"] == pytest.approx(62.75)
    assert rel["economia"] == pytest.approx(11.63)


def test_relatorio_coerente_com_funcoes_da_semana3(itens):
    rel = gerar_relatorio(itens)
    assert rel["total"] == pytest.approx(total_compra(itens))
    assert rel["economia"] == pytest.approx(economia_total(itens))
    assert sum(rel["por_categoria"].values()) == pytest.approx(rel["total"])


def test_relatorio_categoria_ausente_vale_zero():
    rel = gerar_relatorio([Item("Chocolate", 10.00, "padrao")])
    assert rel["por_categoria"]["cesta_basica"] == pytest.approx(0.0)
    assert rel["por_categoria"]["reduzido"] == pytest.approx(0.0)


def test_relatorio_lista_vazia():
    rel = gerar_relatorio([])
    assert rel["total"] == pytest.approx(0.0)
    assert rel["economia"] == pytest.approx(0.0)
    assert all(v == pytest.approx(0.0) for v in rel["por_categoria"].values())


def test_relatorio_nao_altera_lista(itens):
    copia = list(itens)
    gerar_relatorio(itens)
    assert itens == copia
