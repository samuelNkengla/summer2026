import gradio as gr
from transformers import pipeline

# 1. Load a modern, lightweight model optimized for CPU
print("Loading model... (This will download ~1GB the first time)")
# We use Qwen 2.5 0.5B Instruct, which is very fast on CPUs
generator = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", device="cpu")

# 2. Define the prediction function
def generate_response(prompt):
    if not prompt.strip():
        return "Please enter a prompt."
        
    # Modern models use a "chat template" rather than just raw text.
    # We format the input as a conversation between a user and an assistant.
    messages = [
        {"role": "system", "content": "You are a helpful, concise AI assistant."},
        {"role": "user", "content": prompt}
    ]
    
    # Generate the text
    output = generator(
        messages, 
        max_new_tokens=150,  # Allows for a longer, more detailed response
        do_sample=True,      # Adds a bit of creative variance
        temperature=0.7      # Controls the creativity (lower is more focused)
    )
    
    # Extract the generated response specifically from the assistant's turn
    return output[0]['generated_text'][-1]['content']

# 3. Create the GUI using Gradio
app = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, placeholder="Ask me anything..."),
    outputs=gr.Textbox(label="AI Output"),
    title="Modern CPU-Friendly AI",
    description="Running the lightweight Qwen 2.5 model locally on your CPU."
)

# 4. Launch the application
if __name__ == "__main__":
    app.launch()