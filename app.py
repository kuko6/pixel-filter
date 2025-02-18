import gradio as gr

from src.pixelate import pixelate


def update_palette_visibility(use_palette):
    return gr.update(visible=use_palette), gr.update(visible=use_palette)


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

    with gr.Column():
        gr.Markdown("## Examples")
        gr.Examples(
            examples=[
                ["example_images/bananas.jpg", 16, False, True, 8],
                ["example_images/scream.jpg", 16, False, True, 4],
                ["example_images/cat.jpg", 32, True, False, None],
                ["example_images/ducks.jpg", 4, False, True, 2],
            ],
            inputs=[img, pixel_size, blur, use_palette, k],
            outputs=[output_img, output_palette],
            run_on_click=True,
            fn=pixelate,
        )

demo.launch(debug=True)
