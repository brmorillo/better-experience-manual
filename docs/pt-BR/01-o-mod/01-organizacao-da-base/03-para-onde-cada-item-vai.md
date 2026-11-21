# Para onde cada item vai

O item procura primeiro um móvel da subcategoria exata, depois o grupo dele e, por último, **Geral**.

```mermaid
flowchart TD
    A([Item para guardar]) --> B{Móvel da<br>subcategoria?}
    B -->|Sim| G[Guarda lá]
    B -->|Não| C{Móvel do grupo?}
    C -->|Sim| G
    C -->|Não| D{Móvel Geral?}
    D -->|Sim| G
    D -->|Não| E[Fica com você]
```

Exemplos:

- Carne crua: **Carnes cruas** > **Tudo de Congelador** > geladeira > despensa > **Geral**.
- Martelo: **Ferramentas gerais** > **Tudo de Ferramentas** > materiais > **Geral**.

Na comida, as subcategorias vizinhas (geladeira, despensa) também servem de reserva antes do **Geral**.
