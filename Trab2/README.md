Lab 2
=====

Roteiro
-------

Programa em python para fazer análise léxica e sintática de expressões algébricas prefixadas.

Arquivo de entrada
------------------

O seu programa deve ler a entrada da entrada padrão (stdin).

Formato da entrada
------------------

A entrada do programa é uma expressão aritmética prefixada,
em que o operador aparece antes dos argumentos. A gramática é:

    E -> num
    E -> ( E )
    E -> + E E
    E -> - E E
    E -> * E E
    E -> / E E
    E -> ^ E E

- Os aspectos léxicos seguem a tarefa anterior.  
- A entrada pode conter comentários, seguindo o formato da tarefa anterior.  
- Os tokens não precisam estar todos na mesma linha.  
- Os números podem ser escritos em decimal ou em hexadecimal.  
- Números hexadecimais podem usar letras maiúsculas ou minúsculas.

Formato de saída
----------------

Você deve imprimir um número com o resultado da expressão aritmética,  
ou uma mensagem de erro caso a entrada não respeite a gramática.  
Inclua número de linha e coluna na mensagem de erro.

### Mensagens de erro sugeridas:
- Comentário em bloco não terminado
- Esperava token X mas encontrei Y
- Esperava uma expressão mas encontrei token X.
   
Estrutura do parser
-------------------

- O lexer tem um método next(), que dá o próximo token
- O parser deve usar Recursive Descent e produzir uma árvore sintática
- O interpretador recebe a árvore da expressão e calcula o resultado

Modo de uso
-----------

```bash
$ python3 main.py
```
Caso prefira, o programa pode receber a entrada como arquivo:

```bash
$ python3 main.py < input.txt
```
