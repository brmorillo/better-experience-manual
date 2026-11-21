# Safe water

While tap water works, the tap is safe. Once it is shut off, water from rivers, lakes, wells or collected rain can be tainted.

```mermaid
flowchart TD
    A([Got water]) --> B{Tap with<br>running water?}
    B -->|Yes| OK[Safe to drink]
    B -->|No| C{Is it tainted?}
    C -->|No| OK
    C -->|Yes| D[Boil it in a pot<br>on a stove or fire]
    C -->|Yes| E[Purification tablet]
    D --> OK
    E --> OK
```

Hover over the container to see if the water is tainted.

## Still missing

This page is just getting started. Use **Edit this page** to fill in the guide, or **Add a tip** to leave your own trick.
