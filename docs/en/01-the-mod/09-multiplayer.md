# Multiplayer

The mod works on servers. Like any mod, it must be installed **on the server and on every player**.

## What changes in multiplayer

- **Drink from bags**: the character drinks with the game's short animation, because the server is the one that removes thirst. The bottle goes back to the bag afterwards.
- **Safe pause**: nobody can pause a server. Instead of pausing, the mod **warns with a message and a sound** and **turns off automatic fishing and organizing** if they are running. The rule for when it warns is the same as the pause.
- **GPS**: the battery and the glove box GPS are handled by the server. Each car is rolled only once, for every player.
- **Auto fishing**: trash pulled from the water goes to the floor through the game's normal action.

## Where your data is kept

GPS favorites, your track and seen items are kept in a file **on your PC**, one per server and per character:

- `Zomboid/Lua/PersonalAssistant/MP/`

The file is written when the game saves, when you leave the server and every 2 minutes. If you play on another PC, this data does not come along. Furniture categories are stored on the furniture itself, so everyone on the server sees the same ones.

## Server options

Whoever creates the server sets up the GPS in **Server options > Sandbox > Better Experience**:

- **GPS: require a powered GPS** (default: on).
- **GPS: battery life** (default: 48 hours of use, from 6 to 240).
- **GPS: cars with a GPS in the glove box** (default: 1%, from 0 to 5).

In multiplayer these three replace the same mod options. All other mod options stay per player.
