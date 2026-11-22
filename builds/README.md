# Game builds / Builds do jogo

The manual follows the Project Zomboid build. **Build 42 is the base** (`"baseBuild": 42` in [manual.config.json](../manual.config.json)): the [docs/](../docs/) and [tips/](../tips/) folders are the Build 42 manual.

Each newer build gets a folder here **only when something changed**, with **only the files that changed**, at the same path they have in `docs/` and `tips/`:

```
builds/
  43/
    docs/en/02-skills/06-survival/02-fishing.md      <- replaces the Build 42 fishing page
    docs/pt-BR/02-habilidades/06-sobrevivencia/02-pesca.md
    tips/en/fishing.md                               <- tips for the Build 43 fishing page
  44/
    docs/en/03-items/09-new-thing.md                 <- page that only exists from 44 on
```

How the manual of a build is made:

1. Start from the base (`docs/`, `tips/`).
2. Apply each `builds/<N>/` with N up to that build, from the oldest to the newest.
3. A file at the same path **replaces** the inherited one. A new file **adds** a page.
4. A file whose whole text is `<!-- removed -->` **hides** the inherited page in that build and later ones. On a `README.md` it hides the whole section. The start page (`docs/<language>/README.md`) cannot be removed.

So in the example above, Build 44 has everything from 42, the fishing page from 43, and its own new page. A Build 45 with no folder here uses the Build 44 manual.

**Tips** belong to the page version they were written for: the tips of a page from `builds/43/docs/` go in `builds/43/tips/`. The tips of the Build 42 page stay in `tips/`. The in-game **Add a tip** button fills in the right build (`43/en/fishing`).

**In game**, the mod reads the game build and shows the newest manual that is not newer than it.

`python tools/build_manual.py --check` validates every build: folder names must be numbers newer than the base, a `<!-- removed -->` must hide a page that exists in an older build, and tips must sit next to their page's version.

---

🇧🇷 **Português**

O manual acompanha a build do Project Zomboid. **A Build 42 é a base**: as pastas `docs/` e `tips/` são o manual da Build 42.

Cada build nova ganha uma pasta aqui **só quando algo mudou**, com **só os arquivos que mudaram**, no mesmo caminho que eles têm em `docs/` e `tips/`. Exemplo: a Build 43 mudou a pesca → `builds/43/docs/pt-BR/02-habilidades/06-sobrevivencia/02-pesca.md`.

Como o manual de uma build é montado:

1. Começa pela base (`docs/`, `tips/`).
2. Aplica cada `builds/<N>/` com N até aquela build, da mais antiga para a mais nova.
3. Um arquivo no mesmo caminho **troca** o herdado. Um arquivo novo **cria** uma página.
4. Um arquivo cujo texto é só `<!-- removed -->` **esconde** a página herdada naquela build e nas seguintes. Num `README.md`, esconde a seção inteira. A página inicial não pode ser removida.

Assim a Build 44 usa tudo da 42, a pesca da 43 e o que tiver em `builds/44/`. Uma Build 45 sem pasta aqui usa o manual da 44.

**Dicas** ficam com a versão da página: dicas da pesca da Build 43 vão em `builds/43/tips/pt-BR/pesca.md`. O botão **Adicionar dica** do jogo já preenche a build (`43/pt-BR/pesca`).

**No jogo**, o mod lê a build do jogo e mostra o manual mais novo que não passa dela.
