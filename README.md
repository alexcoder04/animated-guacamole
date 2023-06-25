
# animated-guacamole

![Overview](./assets/overview.png)

## *ENGLISH*

Serve live images via http from Raspberry Pi Camera.
The image is taken when you request the page.

### How to use

Download the `main.py` script / clone this repository onto your Raspberry Pi
and run it.

Then, open `http://<your-pi-ip>:8000/` in your browser to see the image
or request `http://<your-pi-ip>:8000/image.jpeg` if you want to get the image
from command line or another script.

### Note

This script uses the legacy picamera module and does not work on newer
64-bit releases of Raspbian.

---

## *DEUTSCH*

Bereitstellung von Live Bildern von der Raspberry Pi Kamera über HTTP.
Das Bild wird in dem Moment geschossen, wenn es angefragt wird.

### Benutzung

Lade das `main.py` Skript herunter oder klone dieses Repository auf deinen
Raspberry Pi und führe es aus.

Öffne `http://<deine-pi-ip>:8000/` im Browser, um das Bild von der Kamera
zu sehen oder frage `http://<deine-pi-ip>:8000/image.jpeg` an, wenn du das Bild
in der Kommandozeile oder in einem anderen Skript benutzen willst.

### Achtung

Dieses Skript verwendet das ältere picamera-Modul, was nicht auf neueren
64-bit-Versionen von Raspbian funktioniert.

---

## Contributors

[@nilswgnr](https://github.com/nilswgnr)
