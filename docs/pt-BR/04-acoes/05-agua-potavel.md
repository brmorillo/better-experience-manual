# Água potável

Enquanto a água encanada funciona, a torneira é segura. Depois que ela é cortada, água de rio, lago, poço ou chuva coletada pode estar contaminada.

```mermaid
flowchart TD
    A([Pegou água]) --> B{Torneira com<br>água encanada?}
    B -->|Sim| OK[Pode beber]
    B -->|Não| C{Está contaminada?}
    C -->|Não| OK
    C -->|Sim| D[Ferver na panela<br>no fogão ou fogueira]
    C -->|Sim| E[Pastilha de purificação]
    D --> OK
    E --> OK
```

Passe o mouse sobre o recipiente para ver se a água está contaminada.

## Ainda falta

Esta página ainda está começando. Use **Editar esta página** para completar o guia, ou **Adicionar dica** para deixar o seu truque.
