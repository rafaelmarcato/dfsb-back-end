from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from typing import Union
from sqlalchemy import CheckConstraint

from  model import Base, Anotacao


class Tarefa(Base):
    __tablename__ = 'tarefa'

    id = Column("pk_tarefa", Integer, primary_key=True)
    nome = Column(String(200))
    descricao = Column(Text)
    status = Column(Integer, default=1)
    data_criacao = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    data_andamento = Column(DateTime)
    data_conclusao = Column(DateTime)

    __table_args__ = (
        CheckConstraint("status IN (1, 2, 3)", name="check_status_range"),
    )

    # Definição do relacionamento entre o tarefa e a anotação.
    # Essa relação é implicita, não está salva na tabela 'tarefa',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    anotacoes = relationship(
        "Anotacao",
        back_populates="tarefa",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __init__(self, nome:str, descricao:str, status:Union[int, None] = None,
                 data_criacao:Union[DateTime, None] = None):
        """
        Cria uma tarefa

        Arguments:
            nome: nome da tarefa
            descricao: descrição da tarefa
            status: status da tarefa (1 - a fazer, 2 - em andamento - 3 concluída)
            data_criacao: data de quando a tarefa foi criada
        """
        self.nome = nome
        self.descricao = descricao
        
        # se não for informado, será o status inicial "1 - a fazer"
        if status:
            self.status = status

        # se não for informada, será o data exata da inserção no banco
        if data_criacao:
            self.data_criacao = data_criacao

    def adiciona_anotacao(self, anotacao:Anotacao):
        """ Adiciona uma nova anotação a Tarefa
        """
        self.anotacoes.append(anotacao)

