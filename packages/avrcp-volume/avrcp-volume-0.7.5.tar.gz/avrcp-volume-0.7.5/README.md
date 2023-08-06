# AVRCP-VOLUME

Avrcp volume controller.

The service provides avrcp volume notifications and infinite avrcp and pulseaudio volume increasing.

## Installation

### aur: `avrcp-volume`

### pip:

```
$ pip install avrcp-volume
$ sudo -E avrcp-volume --install-service
```

## Usage

```
$ systemctl --user start avrcp-volume.service
$ systemctl --user enable avrcp-volume.service
```

Just try to change volume on your headphones. Push avrcp volume using pulseaudio signals(default volume up keybind and other actions) and vice versa.
