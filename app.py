from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from model import Session, Tarefa, Anotacao
from schemas import *
from flask_cors import CORS

info = Info(title="API - Controle de tarefas", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tarefa_tag = Tag(name="Tarefa", description="Adição, visualização e remoção de tarefas à base de dados")
anotacao_tag = Tag(name="Anotacao", description="Adição de um anotação à uma tarefa cadastrada na base de dados")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/tarefa', tags=[tarefa_tag],
          responses={"200": TarefaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tarefa(form: TarefaSchema):
    """Adiciona um nova Tarefa à base de dados

    Retorna uma representação das tarefas e anotações associadas.
    """
    tarefa = Tarefa(
        nome=form.nome,
        descricao=form.descricao)
    try:
        # criando conexão com a base
        session = Session()
        # adicionanda tarefa
        session.add(tarefa)
        
        # efetivando o camando de adição de uma nova tarefa na tabela
        session.commit()
        return apresenta_tarefa(tarefa), 200
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar a nova tarefa :/"
        return {"mesage": error_msg}, 400
    

@app.get('/tarefas', tags=[tarefa_tag],
         responses={"200": ListagemTarefasSchema, "404": ErrorSchema})
def get_tarefas():
    """Faz a busca por todas as Tarefa cadastradas

    Retorna uma representação da listagem de tarefas.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tarefas = session.query(Tarefa).all()

    if not tarefas:
        # se não há tarefas cadastradas
        return {"tarefas": []}, 200
    else:
        # retorna a representação da tarefa
        print(tarefas)
        return apresenta_tarefas(tarefas), 200


@app.get('/tarefa', tags=[tarefa_tag],
         responses={"200": TarefaViewSchema, "404": ErrorSchema})
def get_tarefa(query: TarefaBuscaSchema):
    """Faz a busca por uma tarefa a partir do id da tarefa

    Retorna uma representação das tarefas e anotações associadas.
    """
    tarefa_id = query.id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

    if not tarefa:
        # se a tarefa não foi encontrada
        error_msg = "Tarefa não encontrada na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de tarefa
        return apresenta_tarefa(tarefa), 200


@app.put('/tarefa/<int:id>', tags=[tarefa_tag],
         responses={"200": TarefaViewSchema, "404": ErrorSchema})
def atualiza_tarefa(path: TarefaPathAtualizaSchema, form: TarefaAtualizaSchema):
    """Atualiza uma Tarefa a partir do id da tarefa

    Retorna uma representação das tarefas e anotações associadas.
    """

    tarefa_id = path.id

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

    if not tarefa:
        # se o tarefa não foi encontrado
        error_msg = "Tarefa não encontrada na base :/"
        return {"mesage": error_msg}, 404
    else:

        try:
            #Apenas atualiza a data dos status quando de fato alterar o status
            # 1 - a fazer
            if form.status == 1 and tarefa.status != 1:
                tarefa.data_criacao = datetime.now(timezone.utc)

            # 2 - em andamento
            elif form.status == 2 and tarefa.status != 2:
                tarefa.data_andamento = datetime.now(timezone.utc)

            # 3 - concluído
            elif form.status == 3 and tarefa.status != 3:
                tarefa.data_conclusao = datetime.now(timezone.utc)

            # Atualiza os campos
            tarefa.nome = form.nome
            tarefa.descricao = form.descricao
            tarefa.status = form.status

            session.commit()
            return apresenta_tarefa(tarefa), 200

        except Exception as e:
            error_msg = "Não foi possível atualizar a tarefa :/"
            return {"message": error_msg}, 400
    

@app.delete('/tarefa', tags=[tarefa_tag],
            responses={"200": TarefaDelSchema, "404": ErrorSchema})
def del_tarefa(query: TarefaBuscaSchema):
    """Deleta uma tarefa a partir do id da tarefa informado

    Retorna uma mensagem de confirmação da remoção.
    """
    tarefa_id = query.id
    print(tarefa_id)
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Tarefa).filter(Tarefa.id == tarefa_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Tarefa removida", "id": tarefa_id}
    else:
        # se a tarefa não foi encontrada
        error_msg = "Tarefa não encontrada na base :/"
        return {"mesage": error_msg}, 404


@app.post('/anotacao', tags=[anotacao_tag],
          responses={"200": TarefaViewSchema, "404": ErrorSchema})
def add_anotacao(form: AnotacaoSchema):
    """Adiciona uma nova anotação a uma tarefa cadastrada na base identificada pelo id

    Retorna uma representação das tarefas e anotações associadas.
    """
    tarefa_id  = form.tarefa_id
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo tarefa
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

    if not tarefa:
        # se tarefa não encontrada
        error_msg = "Tarefa não encontrada na base :/"
        return {"mesage": error_msg}, 404

    # criando o anotação
    descricao = form.descricao
    anotacao = Anotacao(descricao)

    # adicionando o anotação a tarefa
    tarefa.adiciona_anotacao(anotacao)
    session.commit()

    # retorna a representação de tarefa
    return apresenta_tarefa(tarefa), 200
