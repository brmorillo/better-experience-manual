# Start the car

Get in the driver's seat. With the key, the car starts. Without it, look in the car itself, on zombies and in nearby houses.

```mermaid
flowchart TD
    A([Found a car]) --> B{Got the key?}
    B -->|Yes| C[Start the car]
    B -->|No| D[Look for the key<br>in the car and nearby]
    D --> E{Found it?}
    E -->|Yes| C
    E -->|No| F[Hotwire]
    F -.-> G[[Needs Electrical and Mechanics<br>or the Burglar occupation]]
    F --> C
```

Before leaving, check the fuel and battery on the dashboard.

## Still missing

This page is just getting started. Use **Edit this page** to fill in the guide, or **Add a tip** to leave your own trick.
