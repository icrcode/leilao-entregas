# leilao-entregas
O escopo deste trabalho contempla os seguintes tópicos: Introdução à IA; Representação do  conhecimento; Teoria dos grafos; Resolução de problemas; Otimização. 

# Inteligência Artificial - Leilão de Entregas - N1

**Professor:** Claudinei Dias (Ney)

## Observações

* O escopo deste trabalho contempla os seguintes tópicos: Introdução à IA; Representação do conhecimento; Teoria dos grafos; Resolução de problemas; Otimização.
* O trabalho deve ser realizado em grupos com no mínimo 3 e no máximo 5 integrantes. Exceções devem ser solicitadas antecipadamente.

## Contexto

Uma startup pretende transformar o setor de entregas urbanas. Ela criou uma proposta onde os clientes oferecem um bônus para que suas entregas sejam priorizadas. A missão da empresa é otimizar a seleção de entregas diárias para maximizar o lucro com base nos bônus. Sua equipe foi contratada para desenvolver uma solução para esse desafio.

## Especificações

1.  O software deve processar duas entradas: Conexões e Entregas.
    * **A.** Uma matriz de conexões entre destinos, junto ao tempo (em minutos) para percorrê-los.
        * Exemplo:
            * (A, B, 5); (B, C, 3); (A, D, 2); (C, D, 8)
        * Esta sequência representa o seguinte mapa:
    * **B.** Uma lista de entregas contendo o horário programado para saída, o destino e o valor do bônus oferecido.
        * Exemplo:
            * Entregas no dia: (0, B, 1); (5, C;10); (10, D, 8).
        * O bônus para entregar em B é 1; para entregar em C é 10, e para entregar em D é 8.
2.  Exemplo do formato do arquivo de entrada das conexões e entregas para 4 conexões.

    ```
    Matriz de Adjacência:
         A,  B,  C,  D
    A    0,  5,  0,  2
    B    5,  0,  3,  0
    C    0,  3,  0,  8
    D    2,  0,  8,  0

    3 entregas agendadas
    0, B, 1
    5, C, 10
    10, D, 8
    ```

3.  Segue interpretação detalhada do exemplo.

    Obs.: para evitar ambiguidade, considerar as seguintes restrições: sempre com partida de A, sempre com carga única e agenda de entrega em minutos, desconsiderar tempo de carga/descarga.

    * Conexões entre destinos e tempos de deslocamento:
        * A-B: 5 minutos
        * B-C: 3 minutos
        * A-D: 2 minutos
        * C-D: 8 minutos
    * Lista de entregas:
        * Entrega em B: início ao 0 minuto, bônus de 1.
        * Entrega em C: início aos 5 minutos, bônus de 10.
        * Entrega em D: início aos 10 minutos, bônus de 8.
    * Analisando as entregas:
        * Opção 1: Entrega em B primeiro
            * Saída de A em 0 minuto, chegada em B em 5 minutos.
            * Retorno a A em mais 5 minutos, totalizando 10 minutos após o início.
            * Dado que a entrega para C começa em 5 minutos, ao escolher a entrega para B primeiro, não poderemos fazer a entrega para C a tempo, pois retornaríamos a A em 10 minutos.
            * A próxima entrega possível seria a entrega para D:
                * Saída de A para D em 10 minutos, chegada em D em 12 minutos.
                * Retorno a A em 14 minutos.
                * Lucro total nesse caso: 1 (B) + 8 (D) = 9 de Bônus.
            * Neste caso, se a primeira entrega for realizada, o tempo para sair do ponto A e chegar em B deve ser considerado no tempo consumido, ou seja, a tarefa começa em 0 e termina em 10 (tempo do retorno). Portanto, a entrega em C já não pode ser mais realizada pois seu tempo de início foi perdido. Sendo possível realizar a entrega para D na sequência, com lucro total de 9.
        * Opção 2: Esperar e fazer a entrega em C
            * Já se a escolha for para esperar a entrega em C, partimos de A em 5 minutos, e as entregas em B e D não poderão ser realizadas, contudo, o lucro será de 10.
            * Para chegar a C, seria A-B (5 minutos) + B-C (3 minutos) = 8 minutos. Portanto, chegada em C em 13 minutos. Dado o tempo de retorno, voltaríamos a A em 21 minutos.
            * Nesse cenário, as entregas para B e D não são mais possíveis devido ao tempo que já passou.
            * Lucro total nesse caso: 10 de bônus.

## Descrição das Tarefas

1.  Desenvolva duas versões deste problema em linguagem de programação Python que seja capaz de:
    * Ler uma lista de conexões.
    * Ler uma lista de entregas.
    * Exibir a sequência de entregas programadas para o dia e o lucro esperado.
        * Versão 1 do Leilão de Entregas: Criar um algoritmo básico, sem a necessidade de cálculos otimizados para obter o melhor resultado entregas e bônus.
        * Versão 2 do Leilão de Entregas: Criar um algoritmo utilizando Inteligência Artificial para encontrar uma solução ótima para este problema (minimizar o tempo e maximizar o bônus).
2.  Resultados.
    * Exemplo de saída: (5, C;10)
    * Faça uma comparação de desempenho entre as duas versões.
    * Elabore gráficos comparativos das soluções A e B detalhando aspectos como tempo de execução e lucro obtido (bônus).
3.  Simulação gráfica do Leilão de Entregas.
    * Crie uma simulação visual interativa dos processos de seleção de entregas (gráficos) que permita que os usuários interajam e modifiquem os parâmetros.
