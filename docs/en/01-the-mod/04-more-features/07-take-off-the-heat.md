# Take food off the heat when done

With the character nearby, food that **finished cooking** goes to the inventory **before it burns**.

## Where it works

Stove, oven, microwave, toaster, wood stove, fireplace, barbecue (charcoal or propane), campfire and brazier.

## How it works

- The character has to be **near**: on the same floor, up to 5 tiles from the heat.
- When the food inside is **cooked** (still hot and not burnt), the character walks to the heat and takes the food out, with the game's normal actions.
- A message shows up: "Food is done: taking it off the heat (Steak)".
- In single player, if the game is sped up, it goes back to normal speed when taking the food out.

## When it only warns

The mod **does not interrupt** you. It only takes the food out when the character is **free**: no action in progress, not walking, not aiming, no zombie nearby and no other automatic task. When it cannot take it out, it warns once and you decide:

- busy: "Steak is done cooking!";
- no room in the inventory: "Steak is done, but there is no room in the inventory!".

With a zombie nearby, it neither takes the food out nor warns.

## In multiplayer

It works the same: it uses the game's normal actions (walking and transferring the item), which the server checks.

## Options

- **Options > Mods > Better Experience - ALL In One > Mod features > Take food off the heat when done**: turns it on and off (default: on).
