import gradio as gr

def chat(message, history):
    return message

gr.ChatInterface(
    fn=chat,
    submit_btn="전송",
    retry_btn=None,
    undo_btn=None,
    clear_btn=None,
    stop_btn=None,
    css="footer{display:none!important}",
).launch(show_api=False)