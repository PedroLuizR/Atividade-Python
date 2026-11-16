"""
Semana 1 — Modelando produtos (Orientação a Objetos)

Complete os trechos marcados com TODO.
Não altere os nomes das classes, métodos e constantes: a correção é automática.
"""

ALIQUOTA_PADRAO = 0.25  # alíquota padrão hipotética (IBS + CBS)


class Produto:
    """Classe base de todos os produtos do supermercado."""

    def __init__(self, nome: str, preco: float):
        self.nome = nome
        # TODO: atribua o preço usando a property (self.preco = preco),
        #       para que a validação do setter também valha na criação.
        pass

    @property
    def preco(self) -> float:
        """Preço do produto SEM imposto."""
        # TODO: retorne o atributo protegido (ex.: self._preco)
        pass

    @preco.setter
    def preco(self, valor: float) -> None:
        # TODO: lance ValueError se o valor for negativo;
        #       caso contrário, guarde em self._preco
        pass

    def aliquota(self) -> float:
        """Cada subclasse define sua própria alíquota."""
        # TODO: lance NotImplementedError (a classe base não tem alíquota)
        pass

    def imposto(self) -> float:
        """Imposto de UMA unidade: round(preco * aliquota, 2)."""
        # TODO
        pass

    def preco_final(self) -> float:
        """Preço + imposto, arredondado em 2 casas."""
        # TODO
        pass

    def __str__(self) -> str:
        """Formato: 'Arroz 5kg - R$ 25.90 (imposto: R$ 0.00)'"""
        # TODO: use f-string com :.2f
        pass


class ProdutoCestaBasica(Produto):
    """Item da Cesta Básica Nacional: alíquota zero."""

    # TODO: sobrescreva aliquota() retornando 0.0
    pass


class ProdutoReduzido(Produto):
    """Alimento com redução de 60%: paga 40% da alíquota padrão."""

    # TODO: sobrescreva aliquota() usando ALIQUOTA_PADRAO
    pass


class ProdutoPadrao(Produto):
    """Produto sem benefício: paga a alíquota padrão."""

    # TODO: sobrescreva aliquota() retornando ALIQUOTA_PADRAO
    pass


if __name__ == "__main__":
    # Área livre para testes manuais
    arroz = ProdutoCestaBasica("Arroz 5kg", 25.90)
    refri = ProdutoPadrao("Refrigerante 2L", 9.00)
    print(arroz)
    print(refri)
