import gradio as gr
import requests
import time

# === Config ===
EC2_PUBLIC_IP = "65.1.91.34"  # Replace this with your actual EC2 public IP
API_URL = f"http://{EC2_PUBLIC_IP}:7860/generate"

def generate(prompt):
    print("[DEBUG] Received prompt from UI:", prompt)

    try:
        print("[DEBUG] Sending POST request to:", API_URL)
        start_time = time.time()

        response = requests.post(API_URL, data={"prompt": prompt}, timeout=3000)

        duration = time.time() - start_time
        print(f"[DEBUG] Response status code: {response.status_code}")
        print(f"[DEBUG] Generation took {duration:.2f} seconds")

        if response.status_code == 200:
            print("[DEBUG] Writing video to 'result.mp4'...")
            with open("result.mp4", "wb") as f:
                f.write(response.content)
            print("[DEBUG] File write complete.")
            return f"Generation complete in {duration:.2f} seconds.", "result.mp4"
        else:
            print("[ERROR] Server responded with error:", response.text)
            return f"Error: {response.text}", None

    except Exception as e:
        print("[EXCEPTION] Request failed:", e)
        return f"Connection failed: {e}", None

with gr.Blocks() as demo:
    gr.Markdown("## 🚀 Text-to-Video Generator")
    prompt = gr.Textbox(label="Enter your video prompt")
    btn = gr.Button("Generate Video")
    status = gr.Textbox(label="Status")
    vid = gr.Video(label="Generated Video")

    btn.click(generate, inputs=prompt, outputs=[status, vid])

print("[INFO] Launching Gradio app...")
demo.launch(server_name="0.0.0.0", server_port=8080)
