# Inventory: All nearby and search

Helpers to find things in the inventory and in the loot window, and to know how long food lasts.

## All nearby

The loot window's container column (the icons on the right) gets one more button, **All nearby**, the last one in the column. It shows in a single list the items of **every nearby container and the floor**.

- It appears when there are **2 or more containers** nearby (not counting the floor).
- The same item in different boxes is grouped in one row, as the game already does.
- The weight in the title is the sum of every container.
- **Taking an item** (double-click, dragging it to the inventory or with right-click) takes it **from its own container**, with the game's normal actions. The character walks to the box if needed.
- **Loot All** under the list: the character goes to each container and takes everything, respecting the weight.
- Taking an item or turning the character to another box **does not take you out** of All nearby.
- Nothing **can be stored** here: dropping items on All nearby does nothing. To store, use the button of the right box. That is why the inventory's **Transfer All** hides while All nearby is open.

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

## Item size

The **Inventory item size** option makes the list's rows and icons smaller (or bigger). See the **Options** page.

## In multiplayer

Works the same: taking an item uses the game's normal actions, which the server checks. All nearby never creates or moves any item by itself.

## Options

- **Options > Mods > Better Experience - ALL In One > Inventory > All nearby button in the loot window**: turns it on and off (default: on).
- **Options > Mods > Better Experience - ALL In One > Inventory > Search bar in the inventories**: turns it on and off (default: on).
- **Options > Mods > Better Experience - ALL In One > Inventory > Freshness bar in the food tooltip**: turns it on and off (default: on).
