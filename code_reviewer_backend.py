import gradio as gr

def basic_code_review(code: str) -> str:
    line_count = len(code.split('\n'))
    char_count = len(code)
    
    keywords = ['def', 'return', 'import', 'for', 'while', 'if', 'else', 'elif']
    keyword_count = {word: code.count(word) for word in keywords}

    keyword_summary = '\n'.join([f"{k}: {v}" for k, v in keyword_count.items() if v > 0])
    
    feedback = f"Lines of code: {line_count}\n" \
               f"Characters: {char_count}\n\n" \
               f"Keywords count:\n{keyword_summary}"

    return feedback

# Setting up the Gradio interface
iface = gr.Interface(
    fn=basic_code_review,
    inputs=gr.inputs.Textbox(lines=20, placeholder="Enter your Python code here..."),
    outputs="text",
    title="Basic CodeReview Assistant",
    description="Paste your Python code below to get a simple analysis!",
)

iface.launch()
