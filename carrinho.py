"""
Semana 2 — O carrinho de compras (Orientação a Objetos: composição)

Complete os trechos marcados com TODO.
Não altere os nomes da classe e dos métodos: a correção é automática.
"""

from produtos import ALIQUOTA_PADRAO, Produto


class Carrinho:
    """Guarda produtos e suas quantidades."""

    def __init__(self):
        # Sugestão: um dicionário  nome -> [produto, quantidade]
        self._itens = {}

    def adicionar(self, produto: Produto, quantidade: int = 1) -> None:
        """
        - TypeError se produto não for instância de Produto
        - ValueError se quantidade não for inteiro >= 1
        - Se já existir produto com o mesmo nome, soma a quantidade
        """
        # TODO
        pass

    def remover(self, nome: str) -> None:
        """Remove o produto inteiro. KeyError se não existir."""
        # TODO
        pass

    def subtotal(self) -> float:
        """Soma de preco * quantidade (sem impostos)."""
        # TODO
        pass

    def total_impostos(self) -> float:
        """Soma de produto.imposto() * quantidade."""
        # TODO
        pass

    def total(self) -> float:
        """subtotal() + total_impostos()"""
        # TODO
        pass

    def economia(self) -> float:
        """
        Quanto o consumidor pagaria A MAIS se todos os produtos
        tivessem a alíquota padrão:
            soma de round(preco * ALIQUOTA_PADRAO, 2) * quantidade
            menos total_impostos()
        """
        # TODO
        pass

    def __len__(self) -> int:
        """Total de UNIDADES no carrinho."""
        # TODO
        pass

    def __contains__(self, nome: str) -> bool:
        """Permite: 'Arroz 5kg' in carrinho"""
        # TODO
        pass


if __name__ == "__main__":
    from produtos import ProdutoCestaBasica, ProdutoPadrao

    c = Carrinho()
    c.adicionar(ProdutoCestaBasica("Feijão 1kg", 8.00), 2)
    c.adicionar(ProdutoPadrao("Chocolate", 10.00))
    print("Total:", c.total())
    print("Economia:", c.economia())
