# Entity: Trello

Trello is a synchronized aggregate board entity stored as `entities/trello/{{ board }}.json`. Board, list, and card IDs are external stable IDs and must never be synthesized.

`Trello new <board>` and `Trello board <board>` create only a local board entity. `Trello sync` mirrors accessible non-archived boards. `Trello <board> sync` mirrors one board. `Trello boards`, `Trello lists`, and `Trello <board> cards` read committed Dru JSON.
