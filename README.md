**!! Atenção: Renomeie o seu repositório para (Tema)_(NomeDoProjeto). !!** 

**Conteúdo da Disciplina**: Grafos 2<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 20/0041606 |  Marina Márcia Costa de Souza |
| 20/0026488 |  Rafael de Medeiros Nobre |

## Sobre 
O projeto é uma interface gráfica e interativa para visualizar os algoritmos de Busca de Árvore Geradora Mínima. Apresenta a execução dos algoritmos:
- MST de Kruskal;
- MST de Prim.


## Screenshots
image1.png
image2.png
image3.png
image4.png

## Instalação 
**Linguagem**: Python 3.9+

Uma vez que o python for instalado, execute o comando abaixo para instalar as dependências:

```cli
pip install -r requirements.txt
````

## Uso 

Para rodar o código, é necessário apontar para um arquivo json que contenha as informações de construção do grafo, a mesma estrutura presente em 'graphs_examples', para executar o código, use o comando:

```cli
python main.py graphs_examples/example2.json kruskal
```
Para executar o algoritmo de kruskal.

e 

```cli
python main.py graphs_examples/example2.json prim
```
Para executar o algoritmo de Prim.
