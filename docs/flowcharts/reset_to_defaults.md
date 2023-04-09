## Reset to Defaults

```mermaid
flowchart TD
    A(Open Reset to Defaults Dialog) -->|Select Items to Reset| B[Ready to Reset]
    B -->|Select Reset| C[Reset Selected Items]
    A -->|Select Cancel| D(Close Dialog)
    B -->|Select Cancel| D(Close Dialog)
    C --> D(Close Dialog)
```

[![Reset to Defaults](../Design/Reset%20to%20Default%20Dialog.png)](../flowcharts/reset_to_defaults.md)
