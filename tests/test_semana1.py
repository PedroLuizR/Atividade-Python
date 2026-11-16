"""Testes da Semana 1 — Produtos (OO). NÃO ALTERE ESTE ARQUIVO."""

import pytest

from produtos import (
    ALIQUOTA_PADRAO,
    Produto,
    ProdutoCestaBasica,
    ProdutoPadrao,
    ProdutoReduzido,
)


# ---------- Constante e estrutura ----------

def test_aliquota_padrao_vale_25_por_cento():
    assert ALIQUOTA_PADRAO == pytest.approx(0.25)


@pytest.mark.parametrize("classe", [ProdutoCestaBasica, ProdutoReduzido, ProdutoPadrao])
def test_subclasses_herdam_de_produto(classe):
    assert issubclass(classe, Produto)


def test_preco_e_uma_property():
    assert isinstance(Produto.__dict__.get("preco"), property)


def test_produto_guarda_nome_e_preco():
    p = ProdutoPadrao("Chocolate", 10.0)
    assert p.nome == "Chocolate"
    assert p.preco == pytest.approx(10.0)


# ---------- Encapsulamento / validação ----------

def test_preco_negativo_na_criacao_lanca_value_error():
    with pytest.raises(ValueError):
        ProdutoPadrao("Chocolate", -1.0)


def test_preco_negativo_na_alteracao_lanca_value_error():
    p = ProdutoPadrao("Chocolate", 10.0)
    with pytest.raises(ValueError):
        p.preco = -5.0
    assert p.preco == pytest.approx(10.0)  # valor antigo preservado


def test_preco_pode_ser_alterado_para_valor_valido():
    p = ProdutoPadrao("Chocolate", 10.0)
    p.preco = 12.0
    assert p.preco == pytest.approx(12.0)
    assert p.imposto() == pytest.approx(3.0)


def test_preco_zero_e_permitido():
    p = ProdutoCestaBasica("Amostra grátis", 0.0)
    assert p.preco == pytest.approx(0.0)


def test_classe_base_nao_define_aliquota():
    p = Produto("Genérico", 10.0)
    with pytest.raises(NotImplementedError):
        p.aliquota()


# ---------- Alíquotas (polimorfismo) ----------

def test_aliquota_cesta_basica_e_zero():
    assert ProdutoCestaBasica("Arroz", 20.0).aliquota() == pytest.approx(0.0)


def test_aliquota_reduzida_e_40_por_cento_da_padrao():
    assert ProdutoReduzido("Iogurte", 6.0).aliquota() == pytest.approx(0.4 * ALIQUOTA_PADRAO)


def test_aliquota_padrao():
    assert ProdutoPadrao("Refrigerante", 9.0).aliquota() == pytest.approx(ALIQUOTA_PADRAO)


def test_polimorfismo_mesmo_metodo_resultados_diferentes():
    produtos = [
        ProdutoCestaBasica("Feijão", 10.0),
        ProdutoReduzido("Iogurte", 10.0),
        ProdutoPadrao("Chocolate", 10.0),
    ]
    impostos = [p.imposto() for p in produtos]
    assert impostos == pytest.approx([0.0, 1.0, 2.5])


# ---------- Cálculos ----------

def test_imposto_cesta_basica_e_calculado_e_vale_zero():
    """Alíquota zero: o cálculo acontece e o resultado é 0.0 (não None)."""
    imposto = ProdutoCestaBasica("Arroz 5kg", 25.90).imposto()
    assert imposto is not None
    assert imposto == pytest.approx(0.0)


def test_imposto_reduzido():
    assert ProdutoReduzido("Iogurte", 7.50).imposto() == pytest.approx(0.75)


def test_imposto_padrao():
    assert ProdutoPadrao("Refrigerante 2L", 9.00).imposto() == pytest.approx(2.25)


def test_imposto_e_arredondado_em_duas_casas():
    # 3.33 * 0.25 = 0.8325 -> 0.83
    assert ProdutoPadrao("Bala", 3.33).imposto() == pytest.approx(0.83)


def test_preco_final_cesta_basica():
    assert ProdutoCestaBasica("Leite 1L", 5.49).preco_final() == pytest.approx(5.49)


def test_preco_final_reduzido():
    assert ProdutoReduzido("Iogurte", 7.50).preco_final() == pytest.approx(8.25)


def test_preco_final_padrao():
    assert ProdutoPadrao("Chocolate", 10.00).preco_final() == pytest.approx(12.50)


# ---------- __str__ ----------

def test_str_cesta_basica():
    assert str(ProdutoCestaBasica("Arroz 5kg", 25.9)) == "Arroz 5kg - R$ 25.90 (imposto: R$ 0.00)"


def test_str_padrao():
    assert str(ProdutoPadrao("Refrigerante 2L", 9)) == "Refrigerante 2L - R$ 9.00 (imposto: R$ 2.25)"
