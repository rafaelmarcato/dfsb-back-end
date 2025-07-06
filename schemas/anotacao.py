from pydantic import BaseModel


class AnotacaoSchema(BaseModel):
    """ Define como uma nova anotação a ser inserida deve ser representada
    """
    tarefa_id: int = 1
    descricao: str = "Descrição da anotação relacionada com a tarefa..."
