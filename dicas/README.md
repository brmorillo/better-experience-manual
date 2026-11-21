# Dicas da comunidade / Community tips

Dicas pessoais de jogadores. **Não fazem parte do guia oficial** (`docs/`), mas aparecem no jogo, no fim da página certa, marcadas como "Dicas da comunidade".

Personal tips from players. **They are not part of the official guide** (`docs/`), but they show in game at the end of the matching page, marked as "Community tips".

## Jeito fácil / Easy way

No jogo, abra a página do manual e clique em **Adicionar dica**. Ou abra um pedido no GitHub com o formulário **Dica da comunidade**. Um robô transforma a dica num pull request, e quem cuida do manual aprova.

In game, open the manual page and click **Add a tip**. Or open a GitHub issue with the **Community tip** form. A bot turns the tip into a pull request, and the manual maintainers approve it.

## Na mão / By hand

Um arquivo por página, com o nome do id da página: `dicas/<idioma>/<id>.md`. O id é o nome do arquivo da página sem o número e sem `.md`. Exemplo: `docs/pt-BR/03-mapa-e-gps/02-gps.md` → `dicas/pt-BR/gps.md`. A página inicial de cada idioma tem o id `inicio`. Uma pasta tem o id do nome dela sem o número.

One file per page, named after the page id: `dicas/<language>/<id>.md`. The id is the page file name without the number and without `.md`. Example: `docs/en/03-map-and-gps/02-gps.md` → `dicas/en/gps.md`. The start page of each language has the id `inicio`. A folder's id is its name without the number.

Cada dica começa com uma linha `## @autor | AAAA-MM-DD` e tem no máximo 600 caracteres. / Each tip starts with a `## @author | YYYY-MM-DD` line and has at most 600 characters.

```markdown
## @seu-usuario | 2026-11-21

Sua dica aqui. Pode usar **negrito**.
```

Como o id não depende da pasta, a comunidade pode mover as páginas do guia à vontade sem perder as dicas. / Since the id does not depend on the folder, the community can move guide pages around without losing their tips.
