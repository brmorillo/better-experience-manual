# Como contribuir / How to contribute

Obrigado por ajudar! / Thanks for helping!

## Português

### Só quero comentar ou avisar de um erro
Abra uma **Issue** (modelos "Correção" ou "Sugestão") ou escreva nas **Discussions**. Não precisa saber Git.

### Quero editar uma página
1. Abra o arquivo em `docs/pt-BR/` (ou `docs/en/`) e clique no lápis ✏️.
2. Faça a mudança e clique em **Propose changes**. O GitHub cria o Pull Request para você.
3. Se puder, atualize também a página no outro idioma. Se não souber, avise no Pull Request que alguém traduz.

### Regras do texto
- Cada arquivo é um capítulo. O número no começo do nome (`01-`, `02-`...) define a ordem.
- A primeira linha é o título: `# Título`.
- Use os nomes **exatos** dos menus e opções do jogo, em **negrito**.
- Frases curtas. Explique o que o jogador faz, não como o código funciona.

### Markdown que aparece no jogo
O manual é convertido para o painel de texto do Project Zomboid, que é simples. Funciona:

- `# Título` (um por arquivo), `## Subtítulo`, `### Subtítulo menor`
- Parágrafos, listas com `-` e listas numeradas `1.`
- `**negrito**` (fica amarelo), `` `código` `` (fica azul), `> dica` (fica verde)
- `[texto](link)`: no jogo aparece só o texto
- `<!-- comentário -->`: não aparece em lugar nenhum

**Não** funciona no jogo: tabelas (o script recusa), imagens e HTML. Evite os sinais `<` e `>` no texto.

### Testar antes de enviar (opcional)
```
python tools/build_manual.py --check
```
O GitHub roda essa mesma verificação em todo Pull Request.

## English

### I only want to comment or report a mistake
Open an **Issue** ("Fix" or "Suggestion" templates) or post in **Discussions**. No Git needed.

### I want to edit a page
1. Open the file in `docs/en/` (or `docs/pt-BR/`) and click the pencil ✏️.
2. Make your change and click **Propose changes**. GitHub creates the Pull Request for you.
3. If you can, update the page in the other language too. If not, say so in the Pull Request and someone will translate it.

### Writing rules
- Each file is a chapter. The number at the start of the name (`01-`, `02-`...) sets the order.
- The first line is the title: `# Title`.
- Use the **exact** names of the game menus and options, in **bold**.
- Short sentences. Explain what the player does, not how the code works.

### Markdown that shows in game
The manual is converted to Project Zomboid's text panel, which is simple. Supported: headings `#`, `##`, `###`, paragraphs, `-` and `1.` lists, `**bold**`, `` `code` ``, `> tip`, `[text](link)` (only the text shows) and `<!-- comments -->`.

**Not** supported in game: tables (the script rejects them), images and HTML. Avoid `<` and `>` in the text.

### Check before sending (optional)
```
python tools/build_manual.py --check
```

## Para o autor do mod / For the mod author

Antes de cada versão do mod / Before each mod release:
```
python tools/build_manual.py --out ../PersonalAssistant/Contents/mods/PersonalAssistant/42/media/lua/client/PersonalAssistant/PA_ManualData.lua
```
