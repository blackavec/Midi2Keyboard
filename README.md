# Midi2Keyboard
A bridge between midi controllers and OS, Midi2Keyboard allows its users to map any key on their midi controller to short cuts on keyboard


## Install
```
make env-setup
source env/bin/activate
make install
```

## Start
```
python3 main.py
```

## App doesn't dispatch the keyboard event on mac?
Mac requires certain permissions, following link will explain it better.
https://github.com/asweigart/pyautogui/issues/247