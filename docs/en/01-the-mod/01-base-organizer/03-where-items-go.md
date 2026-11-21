# Where each item goes

An item first looks for furniture with its exact subcategory, then its group and, last, **General**.

```mermaid
flowchart TD
    A([Item to store]) --> B{Subcategory<br>furniture?}
    B -->|Yes| G[Store it there]
    B -->|No| C{Group furniture?}
    C -->|Yes| G
    C -->|No| D{General furniture?}
    D -->|Yes| G
    D -->|No| E[Stays with you]
```

Examples:

- Raw meat: **Raw meat** > **All Freezer** > fridge > pantry > **General**.
- Hammer: **General tools** > **All Tools** > materials > **General**.

For food, the sibling subcategories (fridge, pantry) also act as backups before **General**.
