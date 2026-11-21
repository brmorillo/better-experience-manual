# Como contribuir / How to contribute

Obrigado por ajudar! / Thanks for helping!

## Português

### Quero deixar uma dica minha
Dicas são truques pessoais ("leia o livro da habilidade antes de treinar"). Elas **não entram no guia oficial**: aparecem no jogo, no fim da página, em **Dicas da comunidade**, com o seu usuário do GitHub.

- **Jeito fácil**: no jogo, abra a página e clique em **Adicionar dica**. Ou abra uma Issue com o modelo **Dica da comunidade**. Um robô coloca a dica no arquivo certo e abre o Pull Request. Não precisa saber Git.
- **Na mão**: veja [dicas/README.md](dicas/README.md).

Até 600 caracteres por dica. Dicas com ofensa, propaganda ou que estragam a surpresa do jogo sem aviso não são aceitas.

### Só quero comentar ou avisar de um erro
Abra uma **Issue** (modelos "Correção" ou "Sugestão") ou escreva nas **Discussions**.

### Quero editar uma página do guia
1. Abra o arquivo em `docs/pt-BR/` (ou `docs/en/`) e clique no lápis ✏️.
2. Faça a mudança e clique em **Propose changes**. O GitHub cria o Pull Request para você.
3. Se puder, atualize também a página no outro idioma. Se não souber, avise no Pull Request que alguém traduz.

### Organizar o manual (pastas)
A árvore de `docs/<idioma>/` **é** a árvore do manual no jogo:

- Cada **pasta** é uma seção. O `README.md` dentro dela é o título e a introdução da seção. Sem `README.md`, o título vem do nome da pasta.
- Cada **arquivo `.md`** é uma página.
- `docs/<idioma>/README.md` é a página inicial.
- O número no começo do nome (`01-`, `02-`...) só define a ordem e não aparece no jogo. Itens sem número vão para o fim, em ordem alfabética.
- Pode ter pastas dentro de pastas.
- Nomes de arquivos e pastas só com letras minúsculas sem acento, números e `-`. Ex.: `03-mapa-e-gps/02-gps.md`.
- O nome sem o número (`gps`) é o **id** da página. Ele não pode se repetir no mesmo idioma, porque é por ele que as dicas encontram a página. Assim você pode **mover** uma página de pasta sem perder as dicas. Se **renomear**, renomeie também `dicas/<idioma>/<id>.md`. O script avisa se esquecer.
- Arquivos e pastas que começam com `_` são ignorados (rascunhos).

Mudanças grandes de estrutura: abra antes uma Discussion para combinar com a comunidade.

### Regras do texto do guia
- A primeira linha é o título: `# Título`.
- Use os nomes **exatos** dos menus e opções do jogo, em **negrito**.
- Frases curtas. Explique o que o jogador faz, não como o código funciona.
- Opinião e truque pessoal vão para as dicas, não para o guia.

### Markdown que aparece no jogo
O manual é convertido para o painel de texto do Project Zomboid, que é simples. Funciona:

- `# Título` (um por arquivo), `## Subtítulo`, `### Subtítulo menor`
- Parágrafos, listas com `-` e listas numeradas `1.`
- `**negrito**` (fica amarelo), `` `código` `` (fica azul), `> dica` (fica verde)
- `[texto](link)`: no jogo aparece só o texto
- `<!-- comentário -->`: não aparece em lugar nenhum

**Não** funciona no jogo: tabelas (o script recusa), imagens e HTML. Evite o sinal `<` no texto.

### Testar antes de enviar (opcional)
```
python tools/build_manual.py --check
```
O GitHub roda essa mesma verificação em todo Pull Request.

## English

### I want to leave a tip
Tips are personal tricks. They **are not part of the official guide**: they show in game at the end of the page, under **Community tips**, with your GitHub user name.

- **Easy way**: in game, open the page and click **Add a tip**. Or open an Issue with the **Community tip** template. A bot puts the tip in the right file and opens the Pull Request. No Git needed.
- **By hand**: see [dicas/README.md](dicas/README.md).

Up to 600 characters per tip. Offensive tips, ads, or spoilers without warning are not accepted.

### I only want to comment or report a mistake
Open an **Issue** ("Fix" or "Suggestion" templates) or post in **Discussions**.

### I want to edit a guide page
1. Open the file in `docs/en/` (or `docs/pt-BR/`) and click the pencil ✏️.
2. Make your change and click **Propose changes**. GitHub creates the Pull Request for you.
3. If you can, update the page in the other language too. If not, say so in the Pull Request and someone will translate it.

### Organizing the manual (folders)
The `docs/<language>/` tree **is** the in-game manual tree:

- Each **folder** is a section. Its `README.md` is the section title and intro. Without one, the title comes from the folder name.
- Each **`.md` file** is a page. `docs/<language>/README.md` is the start page.
- The number at the start of a name (`01-`, `02-`...) only sets the order and is hidden in game. Unnumbered items go last, alphabetically.
- Folders can be nested.
- Names use only lowercase letters without accents, numbers and `-`.
- The name without the number (`gps`) is the page **id**. It must be unique per language, since tips find their page by it. So you can **move** a page to another folder without losing its tips. If you **rename** it, rename `dicas/<language>/<id>.md` too. The script warns you if you forget.
- Files and folders starting with `_` are ignored (drafts).

For big structure changes, open a Discussion first to agree with the community.

### Writing rules for the guide
- The first line is the title: `# Title`.
- Use the **exact** names of the game menus and options, in **bold**.
- Short sentences. Explain what the player does, not how the code works.
- Opinions and personal tricks go to tips, not to the guide.

### Markdown that shows in game
Supported: headings `#`, `##`, `###`, paragraphs, `-` and `1.` lists, `**bold**`, `` `code` ``, `> tip`, `[text](link)` (only the text shows) and `<!-- comments -->`.

**Not** supported in game: tables (the script rejects them), images and HTML. Avoid `<` in the text.

### Check before sending (optional)
```
python tools/build_manual.py --check
```

## Para quem cuida do repositório / For maintainers

- O robô das dicas precisa de: **Settings > Actions > General > Workflow permissions > Allow GitHub Actions to create and approve pull requests**. / The tip bot needs that setting enabled.
- Crie o rótulo `dica` (o formulário usa). / Create the `dica` label (the form uses it).
- Antes de cada versão do mod / Before each mod release:
```
python tools/build_manual.py
```
  Grava `PA_ManualData.lua` na pasta do mod ao lado deste repositório. / Writes `PA_ManualData.lua` into the mod folder next to this repo.
