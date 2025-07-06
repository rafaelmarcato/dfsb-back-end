# API - CONTROLE DE TAREFAS

Projeto **API - Controle de tarefas** referente ao **MVP** da sprint **Desenvolvimento Full Stack Básico** da PUC Rio.

Este projeto permite gerenciar tarefas realizando cadastros, edições, buscas e exclusões. Além disso, é possível criar anotações relacionadas as tarefas, 
as quais são excluídas automaticamente caso a tarefa seja removida.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Para criar o ambiente virtual basta executar:

```
$ python -m venv .venv
```

Para ativar o ambiente virtual, execute:

```
$ .\.venv\Scripts\activate
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

```
(.venv)$ pip install -r requirements.txt
```



Para executar a API  basta executar:

```
(.venv)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(.venv)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/](http://localhost:5000/) no navegador para verificar o status da API em execução.
