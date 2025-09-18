# RainbowBorder for CustomTkinter

Animated rainbow border for CustomTkinter windows.  
Creates a vibrant, animated border cycling through the color spectrum.

## Features

- Customizable border width and animation speed
- Smooth color transitions around the window perimeter
- Easy integration with CustomTkinter apps

## Versions
- RainbowBorder with rounded corners: [Rainbowborder.py](Rainbowborder.py)
- RainbowBorder without rounded corners: [Rainbowborder_wo_rounded_corner.py](Rainbowborder_wo_rounded_corner.py)

## Usage

```python
import customtkinter as ctk
from Rainbowborder import RainbowBorder

root = ctk.CTk()
rainbow_border = RainbowBorder(root, border_width=5)
root.mainloop()
```

## Demo

Run the included demo:

```bash
python Rainbowborder_wo_rounded_corner.py
```

## Requirements

- Python 3.8+
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)

## License

MIT License