# Leilão de Entregas

Este projeto aborda conceitos fundamentais de Inteligência Artificial aplicados à otimização de entregas urbanas. O escopo inclui tópicos como Introdução à IA, Representação do Conhecimento, Teoria dos Grafos, Resolução de Problemas e Otimização.

## Inteligência Artificial - Leilão de Entregas - N1

**Professor:** Claudinei Dias (Ney)

---

## Observações

- O trabalho deve ser realizado em grupos de 3 a 5 integrantes. Exceções devem ser solicitadas previamente.
- O escopo do trabalho inclui tópicos como Introdução à IA, Representação do Conhecimento, Teoria dos Grafos, Resolução de Problemas e Otimização.

---

## Contexto

Uma startup busca revolucionar o setor de entregas urbanas ao permitir que clientes ofereçam bônus para priorizar suas entregas. A missão da equipe é desenvolver uma solução que maximize o lucro diário com base nos bônus oferecidos.

---

## Especificações

### Entradas do Software

1. **Conexões entre destinos**: Uma matriz que representa as conexões e o tempo (em minutos) necessário para percorrê-las.
    - Exemplo:
      ```
      (A, B, 5); (B, C, 3); (A, D, 2); (C, D, 8)
      ```
2. **Lista de entregas**: Contém o horário de saída, o destino e o bônus oferecido.
    - Exemplo:
      ```
      (0, B, 1); (5, C, 10); (10, D, 8)
      ```

### Exemplo de Formato de Entrada

```
Matriz de Adjacência:
      A,  B,  C,  D
A    0,  5,  0,  2
B    5,  0,  3,  0
C    0,  3,  0,  8
D    2,  0,  8,  0

3 entregas agendadas:
0, B, 1
5, C, 10
10, D, 8
```

### Restrições

- Sempre partir do ponto A.
- Apenas uma entrega por vez.
- Agenda de entregas em minutos.
- Desconsiderar tempo de carga/descarga.

---

## Exemplos de Análise

### Opção 1: Priorizar a entrega em B
- Saída de A às 0 minutos, chegada em B às 5 minutos.
- Retorno a A às 10 minutos.
- Próxima entrega possível: D.
- **Lucro total:** 1 (B) + 8 (D) = **9 bônus**.

### Opção 2: Priorizar a entrega em C
- Saída de A às 5 minutos, chegada em C às 13 minutos.
- Retorno a A às 21 minutos.
- Entregas em B e D não são mais possíveis.
- **Lucro total:** 10 (C) = **10 bônus**.

---

## Descrição das Tarefas

1. **Desenvolvimento do Software**
    - **Versão 1:** Algoritmo básico para processar as entregas sem otimização.
    - **Versão 2:** Algoritmo utilizando IA para otimizar o tempo e maximizar o lucro.

2. **Resultados**
    - Exibir a sequência de entregas programadas e o lucro esperado.
    - Comparar o desempenho das duas versões.
    - Criar gráficos comparativos detalhando tempo de execução e lucro obtido.

3. **Simulação Gráfica**
    - Desenvolver uma simulação visual interativa que permita aos usuários modificar parâmetros e observar os resultados.

---

## Exemplo de Saída

```
Sequência de entregas: (5, C, 10)
Lucro total: 10 bônus
```

---

## Objetivo Final

Criar uma solução eficiente e interativa que demonstre a aplicação prática de conceitos de IA na otimização de problemas reais.
