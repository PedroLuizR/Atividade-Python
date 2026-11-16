"""Testes da Semana 2 — Carrinho (OO: composição). NÃO ALTERE ESTE ARQUIVO."""

import pytest

from carrinho import Carrinho
from produtos import ProdutoCestaBasica, ProdutoPadrao, ProdutoReduzido


@pytest.fixture
def carrinho_exemplo():
    """Feijão (cesta) x2, Iogurte (reduzido) x1, Chocolate (padrão) x1."""
    c = Carrinho()
    c.adicionar(ProdutoCestaBasica("Feijão 1kg", 8.00), 2)
    c.adicionar(ProdutoReduzido("Iogurte", 7.50))
    c.adicionar(ProdutoPadrao("Chocolate", 10.00))
    return c


# ---------- Carrinho vazio ----------

def test_carrinho_vazio():
    c = Carrinho()
    assert len(c) == 0
    assert c.subtotal() == pytest.approx(0.0)
    assert c.total_impostos() == pytest.approx(0.0)
    assert c.total() == pytest.approx(0.0)
    assert c.economia() == pytest.approx(0.0)


# ---------- adicionar ----------

def test_adicionar_com_quantidade_padrao_1():
    c = Carrinho()
    c.adicionar(ProdutoPadrao("Chocolate", 10.0))
    assert len(c) == 1


def test_adicionar_mesmo_produto_soma_quantidade():
    c = Carrinho()
    c.adicionar(ProdutoCestaBasica("Arroz 5kg", 25.90), 2)
    c.adicionar(ProdutoCestaBasica("Arroz 5kg", 25.90), 3)
    assert len(c) == 5
    assert c.subtotal() == pytest.approx(129.50)


def test_adicionar_quantidade_zero_lanca_value_error():
    c = Carrinho()
    with pytest.raises(ValueError):
        c.adicionar(ProdutoPadrao("Chocolate", 10.0), 0)


def test_adicionar_quantidade_negativa_lanca_value_error():
    c = Carrinho()
    with pytest.raises(ValueError):
        c.adicionar(ProdutoPadrao("Chocolate", 10.0), -2)


def test_adicionar_quantidade_nao_inteira_lanca_value_error():
    c = Carrinho()
    with pytest.raises(ValueError):
        c.adicionar(ProdutoPadrao("Chocolate", 10.0), 1.5)


def test_adicionar_algo_que_nao_e_produto_lanca_type_error():
    c = Carrinho()
    with pytest.raises(TypeError):
        c.adicionar("Chocolate", 1)


def test_erro_ao_adicionar_nao_altera_carrinho():
    c = Carrinho()
    c.adicionar(ProdutoPadrao("Chocolate", 10.0))
    with pytest.raises(ValueError):
        c.adicionar(ProdutoPadrao("Chocolate", 10.0), 0)
    assert len(c) == 1


# ---------- remover / __contains__ ----------

def test_contains(carrinho_exemplo):
    assert "Feijão 1kg" in carrinho_exemplo
    assert "Picanha" not in carrinho_exemplo


def test_remover_produto(carrinho_exemplo):
    carrinho_exemplo.remover("Feijão 1kg")
    assert "Feijão 1kg" not in carrinho_exemplo
    assert len(carrinho_exemplo) == 2


def test_remover_inexistente_lanca_key_error(carrinho_exemplo):
    with pytest.raises(KeyError):
        carrinho_exemplo.remover("Picanha")


# ---------- Totais ----------

def test_len_conta_unidades(carrinho_exemplo):
    assert len(carrinho_exemplo) == 4


def test_subtotal(carrinho_exemplo):
    # 2 x 8.00 + 7.50 + 10.00
    assert carrinho_exemplo.subtotal() == pytest.approx(33.50)


def test_total_impostos(carrinho_exemplo):
    # feijão 0 + iogurte 0.75 + chocolate 2.50
    assert carrinho_exemplo.total_impostos() == pytest.approx(3.25)


def test_total(carrinho_exemplo):
    assert carrinho_exemplo.total() == pytest.approx(36.75)


def test_economia(carrinho_exemplo):
    # Se tudo fosse padrão: 2 x 2.00 + 1.88 + 2.50 = 8.38 ; cobrado: 3.25
    assert carrinho_exemplo.economia() == pytest.approx(5.13)


def test_economia_exemplo_do_enunciado():
    c = Carrinho()
    c.adicionar(ProdutoCestaBasica("Feijão 1kg", 8.00), 2)
    c.adicionar(ProdutoPadrao("Chocolate", 10.00))
    assert c.total_impostos() == pytest.approx(2.50)
    assert c.economia() == pytest.approx(4.00)


def test_economia_zero_quando_so_produtos_padrao():
    c = Carrinho()
    c.adicionar(ProdutoPadrao("Refrigerante 2L", 9.00), 3)
    assert c.economia() == pytest.approx(0.0)


def test_imposto_calculado_por_unidade_e_multiplicado():
    # imposto unitário: round(3.33 * 0.25, 2) = 0.83 -> 3 x 0.83 = 2.49
    c = Carrinho()
    c.adicionar(ProdutoPadrao("Bala", 3.33), 3)
    assert c.total_impostos() == pytest.approx(2.49)


def test_totais_atualizam_apos_remover(carrinho_exemplo):
    carrinho_exemplo.remover("Chocolate")
    assert carrinho_exemplo.total_impostos() == pytest.approx(0.75)
    assert carrinho_exemplo.total() == pytest.approx(24.25)
