from pydantic import BaseModel,Field, conint
from typing import Optional, List, Literal
from model.tarefa import Tarefa
from datetime import datetime

from schemas import AnotacaoSchema


class TarefaSchema(BaseModel):
    """ Define como uma nova tarefa a ser inserida deve ser representada
    """
    nome: str = "Nova tarefa"
    descricao: str = "Descrição da tarefa..."
    # Status inicial por default sempre 1 - a fazer

class TarefaAtualizaSchema(BaseModel):
    """ Define como uma tarefa a ser atualizada deve ser representada
    """
    nome: str = "Nova tarefa"
    descricao: str = "Descrição da tarefa..."
    status: conint(ge=1, le=3) = Field(..., example=2, description="1=A fazer, 2=Em andamento, 3=Concluído") # type: ignore

class TarefaPathAtualizaSchema(BaseModel):
    """ Define como uma tarefa a ser atualizada deve ser encontrada
    """
    id: int = 1

class TarefaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da terefa.
    """
    id: int = 1


class ListagemTarefasSchema(BaseModel):
    """ Define como uma listagem de tarefas será retornada.
    """
    tarefas:List[TarefaSchema]


def apresenta_tarefas(tarefas: List[Tarefa]):
    """ Retorna uma representação da terefa seguindo o schema definido em
        TarefaViewSchema.
    """
    result = []
    for tarefa in tarefas:

        # 1 - a fazer
        if tarefa.status == 1:
            data_status = tarefa.data_criacao 

        # 2 - em andamento
        elif tarefa.status == 2:
            data_status = tarefa.data_andamento

        # 3 - concluído
        elif tarefa.status == 3:
            data_status = tarefa.data_conclusao

        result.append({
            "id": tarefa.id,
            "nome": tarefa.nome,
            "descricao": tarefa.descricao,
            "status": tarefa.status,
            "data_status" :  data_status,
            "total_anotacoes": len(tarefa.anotacoes)
        })

    return {"tarefas": result}


class TarefaViewSchema(BaseModel):
    """ Define como uma tarefa será retornado: tarefa + anotações.
    """
    id: int = 1
    nome: str = "Nova tarefa"
    descricao: str = "Descrição da tarefa..."
    status: Literal[1, 2, 3]
    total_anotacoes: int = 1
    anotacoes:List[AnotacaoSchema]
    data_status: Optional[datetime] = Field(
        default=None,
        example="2025-06-27T08:00:00"
    )

class TarefaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    mesage: str
    nome: str

def apresenta_tarefa(tarefa: Tarefa):
    """ Retorna uma representação da tarefa seguindo o schema definido em TarefaViewSchema.
    """

    # 1 - a fazer
    if tarefa.status == 1:
        data_status = tarefa.data_criacao 

    # 2 - em andamento
    elif tarefa.status == 2:
        data_status = tarefa.data_andamento

    # 3 - concluído
    elif tarefa.status == 3:
        data_status = tarefa.data_conclusao

    return {
        "id": tarefa.id,
        "nome": tarefa.nome,
        "descricao": tarefa.descricao,
        "status": tarefa.status,
        "data_status" :  data_status,
        "total_anotacoes": len(tarefa.anotacoes),
        "anotacoes": [{"descricao": c.descricao} for c in tarefa.anotacoes]
    }
