# ag-board

## How to use
1. Open `Documents\My Games\WRC\telemetry`
2. Back up `config.json` and the contents of `udp`
3. Replace them with the files from the `gameconfig` folder
4. Run `main.py`

## TODO round 1
- I'm not too happy how the DB handling is done currently, it could use a refactor
- Add some sort of GUI for displaying the runs

## TODO round 2
- Runs should have a metadata field, that can later be edited from a GUI, so we can add data like "input method" or "is in VR"
- There is a channel called `game_delta_time` which apperently contains the time since the last frame. There is also a channel called `game_total_time`. From the two, we should be able to calculate an FPS in the `session_update` package, which could be an interesting run metadata
- id loading could use a refactor
