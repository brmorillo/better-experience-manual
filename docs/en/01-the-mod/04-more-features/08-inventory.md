# Inventory: All nearby and search

Helpers to find things in the inventory and in the loot window, to know how long food lasts and what each book, magazine and tape gives.

## All nearby

The loot window's container column (the icons on the right) gets one more button, **All nearby**, always the **first** one in the column. It shows in a single list the items of **every nearby container and the floor**.

- While it is open, the furniture and boxes in the list are **outlined** in the world, so you can see where the items come from.
- Since it is the first button, the game already opens it when you get near several boxes.
- It appears when there are **2 or more containers** nearby (not counting the floor).
- The same item in different boxes is grouped in one row, as the game already does.
- The weight in the title is the sum of every container.
- **Taking an item** (double-click, dragging it to the inventory or with right-click) takes it **from its own container**, with the game's normal actions. The character walks to the box if needed.
- **Loot All** under the list: the character goes to each container and takes everything, respecting the weight.
- Taking an item or turning the character to another box **does not take you out** of All nearby.
- Nothing **can be stored** here: dropping items on All nearby does nothing. To store, use the button of the right box. That is why the inventory's **Transfer All** hides while All nearby is open.

## Trash

In the character's **inventory**, the last icon of the container column, always stuck to the bottom, is the **Trash**.

- Drag an item to the trash (or open the trash and use the normal actions): it leaves the inventory and **stops weighing**.
- Each item stays there for **10 minutes** (real time). Then it is **gone for good**.
- Within that time you can take it back: open the trash and drag the item to the inventory or a bag.
- Hover the icon to see how many items it has and how much time is left.
- It does not accept **favorite** items, **equipped** items (in hand or worn) or items on the **hotbar**. Only items from the character's inventory.
- Leaving the game or dying **empties** the trash.

## Search

The title bar of the **inventory** and of the **loot window** has a **Search...** box. Type and the list only shows what matches.

- **No accents** needed and case does not matter.
- Finds items by their name in **English and in the game's language** and by **category** ("food", "tool"...).
- **Several words** narrow it down: "can beans".
- Together with **All nearby**, it searches every nearby box at once.
- The search stays when you switch containers. To see everything again, clear the text (or click the X in the box).
- It only changes what the list shows: items do not move.
- When the window is very narrow, the box hides so it does not cover the title.

## Freshness bar on food

The game only says in the name if food is **Fresh**, **Stale** or **Rotten**. With this option, the food tooltip (hover the item) gets two more lines at the end:

- **Freshness** with a bar: green while fresh, orange after it goes stale. The bar empties until the next stage.
- The time left: **Fresh for 3 days more** or **Spoils in 20 h**. Under 2 days it is shown in hours.
- In a **powered fridge** (generator or the grid still on) the count already uses the slower fridge rate and shows **(in the fridge)**.
- **Frozen: does not spoil** when the food is frozen in the freezer. Blue bar.
- Follows your save's sandbox **food rot speed** and **fridge efficiency**.
- Food that never spoils (closed canned food, for example), rotten or burnt food shows no bar.
- It is an estimate for where the item is right now: taking it out of the fridge makes time run faster.

**Who sees the bar:** only characters who know food. The bar shows if the character has the **Nutritionist** trait, has **Cooking 5** or more, or has read the rare magazine **Food Freshness Guide**. The magazine is very hard to find: cooking bookstores, kitchen book shelves, magazine racks and libraries.

## Books, magazines, VHS and CDs

The game's tooltip says little: a skill book only says it gives an "XP multiplier", and a VHS or CD says nothing at all. With this option the tooltip gets lines at the end saying what the item gives:

- **Skill book**: the bonus and the levels, for example **XP bonus x3 in Carpentry, levels 1 to 2**. Below it, whether it fits your character now: **Good for your level**, **Too advanced** (says which level it needs) or **Too basic**.
- **Recipe magazine**: how many recipes are new to you (**2 of 5 recipes are new to you**) or **You already know every recipe here**.
- **VHS and CD**: the XP of each skill (**XP: Carpentry +450**), the recipes it teaches, what it reduces (boredom, stress...) and how much you have already watched. Parts you already watched give no XP again, so the number counts only what is left.
- The game only gives VHS XP while the skill is below a level set in the sandbox (3 by default). The tooltip warns about it and shows **only up to level 3** when you are already past it.
- Tapes with no XP show **No XP: just entertainment**.

## Item size

The **Inventory item size** option makes the list's rows and icons smaller (or bigger). See the **Options** page.

## In multiplayer

Works the same: taking an item uses the game's normal actions, which the server checks. All nearby never creates or moves any item by itself.

## Options

- **Options > Mods > Better Experience - ALL In One > Inventory > All nearby button in the loot window**: turns it on and off (default: on).
- **Options > Mods > Better Experience - ALL In One > Inventory > Search bar in the inventories**: turns it on and off (default: on).
- **Options > Mods > Better Experience - ALL In One > Inventory > Freshness bar in the food tooltip**: turns it on and off (default: on).
- **Options > Mods > Better Experience - ALL In One > Inventory > Better tooltip for books, magazines, VHS and CDs**: turns it on and off (default: on).
- **Options > Mods > Better Experience - ALL In One > Inventory > Trash in the inventory**: turns it on and off (default: on).
