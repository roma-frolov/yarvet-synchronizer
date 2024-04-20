class ProductNotFoundError(Exception):
    def __init__(self, product_id: int) -> None:
        super().__init__(f"{product_id=} is not found")
