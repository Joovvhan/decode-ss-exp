# Decode Soongsil Experiments

### HOWTO
1. Place .txt files in this directory
2. python main.py
3. .csv files will be created

### SAMPLES

Button pressed message

![](./imgs/button_pressed.png)

Button released message

![](./imgs/button_released.png)

Sound event form Person ID 3 (Zig)

![](./imgs/sound_event.png)

![](./imgs/person_id.png)



### TODO

- [x] Change z and y coordinate from the zig.

- [x] Handles multiple .txt files at once.

- [ ] Check whether the coordinate is left handed frame or right handed.

- [x] Check sound event does not cause any decoding errors.

- [x] Add line breaking when a button event occurs.
