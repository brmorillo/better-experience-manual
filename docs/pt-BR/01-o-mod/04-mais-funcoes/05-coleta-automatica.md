# Coleta automática

Com o **modo de busca** do jogo ligado, o personagem anda sozinho até os itens que a busca achou e pega cada um, sempre perto de onde começou. É o mesmo que dar clique duplo em cada ícone, só que sem você precisar clicar.

## Como ligar

- **Clique direito no chão** > **Better Experience - ALL In One** > **Coletar sozinho por perto**. Aparece quando a busca do jogo está ligada.
- **Clique direito num ícone achado pela busca** > **Coletar sozinho**:
  - **Tudo do filtro**: pega o que passa no filtro das opções;
  - **Só** (nome do item): pega só aquele item;
  - **Só a categoria** (nome da categoria): pega só aquela categoria, como amoras ou cogumelos.
- **Tecla** de atalho **Coleta automática / parar** (sem tecla de fábrica). Ela liga a busca do jogo se precisar.

Aparece a mensagem: "Coleta automática ligada (Só comida). Ande para parar."

## O que o personagem faz

- Vai no item **mais perto** que passa no filtro, dentro do raio, e pega.
- Quando a busca só **notou** algo (o ícone de **olho**), ele anda até perto do olho e espera um pouco para a busca revelar o que é. Se for algo do filtro, pega. Ele tenta o mesmo olho no máximo duas vezes.
- Sem nada à vista, para alguns segundos olhando em volta e anda para outro ponto dentro do raio, para a busca achar mais.
- Nunca passa do **raio** em volta de onde começou (padrão: 10 tiles).
- Plantas que o personagem **sabe** que são venenosas ficam de fora, a não ser que você escolha pegar só aquele item.

## Auto descartar

Opção desligada por padrão. Ligada, os itens que a busca revela e que **não passam no filtro** somem da busca, em vez de ficarem na tela. Exemplo: coletando só comida, os galhos e pedras revelados somem.

O item descartado **não é pego**: ele só sai da busca. No multiplayer ele some só para você.

Ao parar, aparece também: "Itens descartados da busca: 3".

## Quando para

A coleta para sozinha, com a mensagem do motivo:

- você **anda** (qualquer tecla de movimento);
- um zumbi **persegue** o personagem ou chega muito perto;
- a **busca do jogo desliga** (o próprio jogo desliga a busca com zumbi perto ou correndo);
- o personagem fica **cansado** demais;
- **não cabe** mais nada no inventário;
- o personagem entra num **veículo**.

No fim aparece quantos itens foram pegos: "Coleta automática desligada. Itens pegos: 5".

## O que ela não faz

- **Não acelera o jogo**: a busca do jogo só acha itens na velocidade normal.
- Não corre: anda, para não fazer barulho nem desligar a busca.

## No multiplayer

Usa só as ações normais do jogo (andar e pegar o item achado), que o servidor confere. O auto descartar some com o ícone só na sua tela.

## Opções

- **Opções > Mods > Better Experience - ALL In One > Funções do mod > Coleta automática**: liga e desliga.
- **Tarefas automáticas > Raio da coleta automática**: de 3 a 25 tiles (padrão: 10).
- **Tarefas automáticas > O que a coleta automática pega**: tudo, tudo menos lixo, só comida, só isca de pesca, só medicinal ou só materiais (lenha, pedras...). Padrão: tudo.
- **Tarefas automáticas > Auto descartar**: desligado por padrão.
- **Teclas de atalho > Coleta automática / parar**: sem tecla de fábrica.
