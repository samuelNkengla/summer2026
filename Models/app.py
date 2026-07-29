# Simple language model app built using assistance from Google Gemini 7/28/2026

import gradio as gr 
from transformers import pipeline 

""" A. Load Language Model """
# Model used: GPT-2 ( USed for small size and ease of use on CPU models without GPU )

print("Loading model... ")
generator = pipeline('text-generation', model = 'gpt2')

""" B. Prediction function """
def generate_response(prompt):
    """
    Take the user's input and feed it into the model. The model returns the output
    """
    if not prompt.strip():
        return "Please enter a prompt"

    # Generate text. max_new_tokens controls how much text is generated.
    # We set pad_token_id to avoid a common warning with GPT-2 ( Tells the model which token to use for padding sequences to equal length. )
    output = generator(prompt, max_new_tokens=50, pad_token_id=50256)

    # Extract text from model output dictionary ( Will experiment with other output options ) 
    return output[0]['generated_text']

""" C. Create the GUI using Graio """
app = gr.Interface(
    fn=generate_response, # The function to run 
    inputs=gr.Textbox(lines=4, placeholder="Type prompt here..."), # Input box 
    outputs=gr.Textbox(label="AI Output"), # Output box
    title="Simple Python Language Model",
    description="A simple interface for generating text using the GPT-2 model."
)

""" D. Launch the application """
if __name__ == "__main__":
    app.launch()