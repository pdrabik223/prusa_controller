# prusa_controller


Repo contains:
1. pc-prusa live interface - Done
    - submarine steering pad controls - Done
    - terminal gcode injection - Done
    - from file gcode runner - In Progres


2. gcode-file composer
3. gcode-file   

# TODO
~~1. Improve pad state display~~
~~2. Test new pad soft on the printer~~
3. Pad controls very aggressively utilizes cpu, some other game pad library should be used  
4. Basic Info panel in browser
5. 

# [Gcode commands](https://help.prusa3d.com/article/prusa-firmware-specific-g-code-commands_112173)
[RepRap](https://reprap.org/wiki/G-code#M114:_Get_Current_Position)

[M400 - Wait for all moves to finish](https://help.prusa3d.com/article/prusa-firmware-specific-g-code-commands_112173#:~:text=M400%20%2D%20Wait%20for%20all%20moves%20to%20finish%20M400%3A%20Wait%20for%20current%20moves%20to%20finish)

[M300 - Play tone](https://help.prusa3d.com/article/prusa-firmware-specific-g-code-commands_112173#:~:text=%2D%20Target%20position-,M300%20%2D%20Play%20tone,-M300%3A%20Play%20beep)

[M117 - Display Message M117: Display Message](https://help.prusa3d.com/article/prusa-firmware-specific-g-code-commands_112173#:~:text=M117%20%2D%20Display%20Message%20M117%3A%20Display%20Message)