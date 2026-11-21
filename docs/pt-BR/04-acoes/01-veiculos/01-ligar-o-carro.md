# Ligar o carro

Entre no banco do motorista. Com a chave, o carro liga. Sem a chave, procure no próprio carro, nos zumbis e nas casas perto.

```mermaid
flowchart TD
    A([Achou um carro]) --> B{Tem a chave?}
    B -->|Sim| C[Ligar o carro]
    B -->|Não| D[Procurar a chave<br>no carro e por perto]
    D --> E{Achou?}
    E -->|Sim| C
    E -->|Não| F[Ligação direta]
    F -.-> G[[Precisa saber Elétrica e Mecânica<br>ou ser Ladrão]]
    F --> C
```

Antes de sair, olhe o combustível e a bateria no painel.

## Ainda falta

Esta página ainda está começando. Use **Editar esta página** para completar o guia, ou **Adicionar dica** para deixar o seu truque.
