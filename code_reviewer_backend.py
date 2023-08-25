import gradio as gr


def basic_code_review(code: str) -> str:
    lines = code.split('\n')
    line_count = len(lines)
    char_count = len(code)

    keywords = ['def', 'return', 'import',
                'for', 'while', 'if', 'else', 'elif']
    keyword_count = {word: code.count(word) for word in keywords}

    function_count = code.count('def ')
    comment_count = sum(1 for line in lines if line.strip().startswith("#"))
    comment_ratio = comment_count / line_count if line_count != 0 else 0

    long_lines = [line for line in lines if len(line) > 79]

    feedback = []
    feedback.append(f"Lines of code: {line_count}")
    feedback.append(f"Characters: {char_count}")
    feedback.append("\nKeywords count:")
    for k, v in keyword_count.items():
        if v > 0:
            feedback.append(f"{k}: {v}")

    feedback.append(f"\nNumber of functions: {function_count}")
    feedback.append(
        f"Comment ratio (comments/total lines): {comment_ratio:.2f}")

    if long_lines:
        feedback.append("\nCoding style issues:")
        feedback.append("Some lines are too long (more than 79 characters).")

    # Basic code quality check
    if line_count > 300:
        feedback.append(
            "\nThe code is quite long. Consider modularizing or refactoring.")
    if function_count == 0:
        feedback.append(
            "No functions found. Consider using functions/methods to organize your code better.")
    if comment_ratio < 0.1:
        feedback.append(
            "Low comment ratio. Consider adding more comments for clarity.")

    return "\n".join(feedback)


# Setting up the Gradio interface
iface = gr.Interface(
    fn=basic_code_review,
    inputs=gr.inputs.Textbox(
        lines=20, placeholder="Enter your Python code here..."),
    outputs="text",
    title="Advanced CodeReview Assistant",
    description="Paste your Python code below to get an advanced analysis!",
)

iface.launch()
