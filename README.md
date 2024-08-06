# ag-board

## How to use
1. Open `Documents\My Games\WRC\telemetry`
2. Back up `config.json` and the contents of `udp`
3. Replace them with the files from the `gameconfig` folder
4. Run `main.py`

## Tips for making changes
- Configure different packet types in `telemetry\udp\some_name.json`
- For possible packet lifecycles (`id` field in `some_name.json \ packets`) see the PDF Scopes & Packets section
- When setting up `telemetry\config.json` it makes things easier if each packet is on a different port
- The PDF says that setting the `frequencyHz` field to 0 will disable it, but instead that makes it so it only goes out once, which is important for the start and stop packets
- The PDF says that the `enabled` field enables a packet, but actually it is the `bEnabled` field

## TODO round 1
- Add some sort of GUI for displaying the runs

## TODO round 2
- Runs should have a metadata field, that can later be edited from a GUI, so we can add data like "input method" or "is in VR"
- There is a channel called `game_delta_time` which apperently contains the time since the last frame. There is also a channel called `game_total_time`. From the two, we should be able to calculate an FPS in the `session_update` package, which could be an interesting run metadata
- id loading could use a refactor
- DB handling could use a refactor
