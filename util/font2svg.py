import gradio as gr

def font2svg(pathToFont):
    gr.Info("Преобразование завершено!")
    return (
            gr.Button("Сохранить",interactive=True), 
            gr.Button("Отправить на генерацию", interactive=True)
            )