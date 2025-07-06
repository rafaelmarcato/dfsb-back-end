from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from typing import Union

from  model import Base


class Anotacao(Base):
    __tablename__ = 'anotacao'

    id = Column(Integer, primary_key=True)
    descricao = Column(Text)
    data_criacao = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Definição do relacionamento entre a anotação e uma tarefa.
    # Aqui está sendo definida a coluna 'tarefa_id' que vai guardar referência a tarefa, 
    # a chave estrangeira que relaciona uma tarefa a anotação.
    tarefa_id = Column(Integer, ForeignKey("tarefa.pk_tarefa", ondelete="CASCADE"), nullable=False)

    tarefa = relationship("Tarefa", back_populates="anotacoes")

    def __init__(self, descricao:str, data_criacao:Union[DateTime, None] = None):
        """
        Cria uma anotação

        Arguments:
            descricao: a descrição de uma anotação
            data_criacao: data de quando a anotação foi criada
        """
        self.descricao = descricao
        if data_criacao:
            self.data_criacao = data_criacao
