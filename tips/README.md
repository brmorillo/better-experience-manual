# Community tips / Dicas da comunidade

Personal tips from players. **They are not part of the official guide** (`docs/`), but they show in game at the end of the matching page, marked as "Community tips".

> 🇧🇷 Dicas pessoais de jogadores. **Não fazem parte do guia oficial** (`docs/`), mas aparecem no jogo, no fim da página certa, marcadas como "Dicas da comunidade".

## Easy way / Jeito fácil

In game, open the manual page and click **Add a tip**. Or open a GitHub issue with the **Community tip** form. A bot turns the tip into a pull request, and the manual maintainers approve it.

> 🇧🇷 No jogo, abra a página do manual e clique em **Adicionar dica**. Ou abra uma Issue com o formulário **Community tip**. Um robô transforma a dica num pull request, e quem cuida do manual aprova.

## By hand / Na mão

One file per page, named after the page id: `tips/<language>/<id>.md`. The id is the page file name without the number and without `.md`. Example: `docs/en/01-the-mod/03-map-and-gps/02-gps.md` → `tips/en/gps.md`. The start page of each language has the id `inicio`. A folder's id is its name without the number.

Each tip starts with a `## @author | YYYY-MM-DD` line and has at most 600 characters.

```markdown
## @your-user | 2026-11-21

Your tip here. **Bold** works.
```

Since the id does not depend on the folder, the community can move guide pages around without losing their tips.

> 🇧🇷 Um arquivo por página, com o nome do id da página: `tips/<idioma>/<id>.md`. O id é o nome do arquivo da página sem o número e sem `.md`. Exemplo: `docs/pt-BR/01-o-mod/03-mapa-e-gps/02-gps.md` → `tips/pt-BR/gps.md`. A página inicial tem o id `inicio`. Cada dica começa com uma linha `## @autor | AAAA-MM-DD` e tem no máximo 600 caracteres. Como o id não depende da pasta, dá para mover as páginas sem perder as dicas.
