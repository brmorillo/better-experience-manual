# Auto foraging

With the game's **search mode** on, the character walks on its own to the items the search found and picks each one up, always near where it started. It is the same as double-clicking each icon, without you having to click.

## How to start

- **Right-click the ground** > **BetterExperience** > **Forage around here by myself**. It shows up when the game's search mode is on.
- **Right-click an icon found by the search** > **Forage by myself**:
  - **Everything in the filter**: picks up what passes the filter in the options;
  - **Only** (item name): picks up only that item;
  - **Only the category** (category name): picks up only that category, such as berries or mushrooms.
- The **Auto foraging / stop** hotkey (no key by default). It turns the game's search mode on if needed.

A message shows up: "Auto foraging on (Food only). Walk to stop."

## What the character does

- Goes to the **nearest** item that passes the filter, inside the radius, and picks it up.
- When the search only **noticed** something (the **eye** icon), it walks close to the eye and waits a bit for the search to reveal what it is. If it passes the filter, it picks it up. It tries the same eye at most twice.
- With nothing in sight, it stops for a few seconds looking around and walks to another spot inside the radius, so the search finds more.
- It never goes past the **radius** around where it started (default: 10 tiles).
- Plants the character **knows** are poisonous are skipped, unless you chose to pick up only that item.

## Auto discard

Off by default. When on, items the search reveals that **do not pass the filter** disappear from the search instead of staying on screen. Example: foraging food only, the twigs and stones it reveals disappear.

The discarded item is **not picked up**: it only leaves the search. In multiplayer it disappears only for you.

When it stops, you also see: "Items discarded from the search: 3".

## When it stops

Foraging stops on its own, with a message saying why:

- you **walk** (any movement key);
- a zombie **chases** the character or gets very close;
- the **game's search mode turns off** (the game itself turns it off with a zombie nearby or when running);
- the character gets too **tired**;
- nothing else **fits** in the inventory;
- the character gets into a **vehicle**.

At the end it shows how many items were picked up: "Auto foraging off. Items picked up: 5".

## What it does not do

- **It does not speed up the game**: the game's search only finds items at normal speed.
- It does not run: it walks, so it makes no noise and does not turn the search off.

## In multiplayer

It only uses the game's normal actions (walking and picking up the found item), which the server checks. Auto discard removes the icon only from your screen.

## Options

- **Options > Mods > Better Experience - ALL In One > Mod features > Auto foraging**: turns it on and off.
- **Automatic tasks > Auto foraging radius**: from 3 to 25 tiles (default: 10).
- **Automatic tasks > What auto foraging picks up**: everything, everything but junk, food only, fishing bait only, medicinal only or materials only (firewood, stones...). Default: everything.
- **Automatic tasks > Auto discard**: off by default.
- **Hotkeys > Auto foraging / stop**: no key by default.
