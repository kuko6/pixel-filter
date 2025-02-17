import cv2
import gradio as gr
import numpy as np


def sort_by_brightness(palette: np.uint8):
    # https://stackoverflow.com/a/596241
    luminosity = (
        0.2126 * palette[:, 2] + 0.7152 * palette[:, 1] + 0.0722 * palette[:, 0]
    )
    return palette[np.argsort(luminosity)]


def display_palette(palette: np.uint8, sort=True):
    swatch_size = 100
    num_colors = palette.shape[0]
    palette_image = np.zeros((swatch_size, swatch_size * num_colors, 3), dtype=np.uint8)

    if sort:
        palette = sort_by_brightness(palette)

    for i, color in enumerate(palette):
        palette_image[:, i * swatch_size : (i + 1) * swatch_size] = color

    return palette_image


def extract_color_palette(img, k: int):
    pixels = img.reshape((-1, 3))
    pixels = np.float32(pixels)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(
        pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    palette = np.uint8(centers)
    return palette, labels


def pixelate(img, pixel_size: int, blur=False, use_palette=False, k=8):
    palette = None
    if use_palette:
        palette, labels = extract_color_palette(img, k)
        res = palette[labels.flatten()]
        img = res.reshape((img.shape))
        palette = display_palette(palette, sort=True)

    if blur:
        img = cv2.blur(img, (7, 7))

    for i in range(0, img.shape[0], pixel_size):
        for j in range(0, img.shape[1], pixel_size):
            img[i : i + pixel_size, j : j + pixel_size] = img[i][j]

    return img, palette


def update_palette_visibility(use_palette):
    return gr.update(visible=use_palette),  gr.update(visible=use_palette)


with gr.Blocks() as demo:
    gr.Markdown("# Simple Pixelart Filter")

    with gr.Row(equal_height=True):
        with gr.Column(variant="panel"):
            img = gr.Image(label="Input Image")
            pixel_size = gr.Number(label="Pixel Size", minimum=1, value=16)
            blur = gr.Checkbox(label="Blur")
            use_palette = gr.Checkbox(label="Use Palette")
            k = gr.Number(label="Number of Colours", minimum=2, value=8, visible=False)

        with gr.Column(variant="panel"):
            output_img = gr.Image(
                label="Output Image", format="jpeg", show_share_button=True
            )
            output_palette = gr.Image(
                label="Image Palette",
                show_download_button=False,
                show_share_button=False,
                visible=False,
            )

        use_palette.change(
            fn=update_palette_visibility,
            inputs=use_palette,
            outputs=[output_palette, k],
        )

    btn = gr.Button("Pixelate", variant="primary")
    btn.click(
        fn=pixelate,
        inputs=[img, pixel_size, blur, use_palette, k],
        outputs=[output_img, output_palette],
    )

    btn_clear = gr.ClearButton(
        components=[img, blur, output_img, output_palette, use_palette]
    )

demo.launch(debug=True, pwa=True)
