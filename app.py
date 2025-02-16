import gradio as gr
import cv2


def pixelate(img, pixel_size: int, blur=False):
    if blur:
        img = cv2.blur(img, (7, 7))

    for i in range(0, img.shape[0], pixel_size):
        for j in range(0, img.shape[1], pixel_size):
            img[i : i + pixel_size, j : j + pixel_size] = img[i][j]

    return img


with gr.Blocks() as demo:
    gr.Markdown("# Simple Pixelart Filter")
    with gr.Row():
        with gr.Column(variant="panel"):
            img = gr.Image(label="Input Image")
            pixel_size = gr.Number(label="Pixel Size", minimum=1, value=16)
            blur = gr.Checkbox(label="Blur")
        with gr.Column():
            output = gr.Image(
                label="Output Image", format="jpeg", show_share_button=True
            )

    with gr.Column():
        btn = gr.Button("Pixelate", variant="primary")
        btn.click(fn=pixelate, inputs=[img, pixel_size, blur], outputs=output)
        btn_clear = gr.ClearButton(components=[img, blur, output])

demo.launch(debug=True, pwa=True)
