# Multiplayer

O mod funciona em servidores. Ele precisa estar instalado **no servidor e em todos os jogadores**, como qualquer mod.

## O que muda no multiplayer

- **Beber da mochila**: o personagem bebe com a animação curta do jogo, porque quem tira a sede é o servidor. A garrafa volta para a bolsa depois.
- **Pausa com zumbi perto**: ninguém pode pausar um servidor. No lugar da pausa, o mod **avisa com mensagem e som** e **desliga a pesca automática e a organização**, se estiverem rodando. A regra de quando avisar é a mesma da pausa.
- **GPS**: a pilha e o GPS do porta-luvas são cuidados pelo servidor. Cada carro sorteia uma vez só, para todos os jogadores.
- **Pesca automática**: o lixo que sai da água vai para o chão pela ação normal do jogo.
- **Coleta automática**: usa as ações normais do jogo (andar e pegar o item achado). O **Auto descartar** some com o item só na sua tela.
- **Tirar do fogo quando ficar pronto**: funciona igual, com as ações normais do jogo.
- **Acelerar tarefas automáticas**: não funciona, porque ninguém muda a velocidade de um servidor.

## Onde ficam os seus dados

Favoritos do GPS, trajeto e itens vistos ficam num arquivo **no seu PC**, separado por servidor e por personagem:

- `Zomboid/Lua/PersonalAssistant/MP/`

O arquivo é gravado quando o jogo salva, ao sair do servidor e a cada 2 minutos. Se você jogar em outro PC, esses dados não vão junto. As categorias dos móveis ficam no próprio móvel, então todos do servidor veem as mesmas.

## Opções do servidor

Quem cria o servidor ajusta o GPS em **Opções do servidor > Sandbox > Better Experience**:

- **GPS: exigir GPS com pilha** (padrão: ligado).
- **GPS: duração da pilha** (padrão: 240 horas de uso, de 6 a 240).
- **GPS: carros com GPS no porta-luvas** (padrão: 0,5%, de 0 a 5).

No multiplayer, essas três valem no lugar das mesmas opções do mod. As outras opções do mod continuam sendo de cada jogador.
