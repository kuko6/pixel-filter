# Simple Pixelart Filter
A Gradio [app](https://kuko6-pixel-filter.hf.space/) that allows you to pixelate images, quantize colors and display color palettes.

<p align="center">
    <img src="example_images/bananas.jpg" alt="Bananas" width="30%">
    <img src="example_images/bananas_out.jpeg" alt="Bananas pixelated" width="30%">
    <img src="example_images/bananas_palette.jpeg" alt="Bananas palette" width="30%">
</p>

<!-- ## Features
- Pixelate images with customizable pixel size
- Apply blur effect to pixelated images
- Quantize  using k-means clustering
- Interactive web interface using Gradio -->

## Try it locally
set up a virtual environment with:
```sh
python3 -m venv venv
```

activate the virtual environment:
```sh
source venv/bin/activate
```

install the requirements:
```sh
pip install -r requirements.txt
```

run the gradio app:
```sh
python3 app.py
```

open `127.0.0.1:7860` in your browser.