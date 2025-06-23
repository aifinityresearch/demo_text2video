from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import subprocess
import time
import os

app = FastAPI()
OUTPUT_DIR = "/home/aifinity/Wan2.1/outputs"
MODEL_PATH = "/home/aifinity/Wan2.1/models/Wan2.1-T2V-1.3B"
SCRIPT_PATH = "/home/aifinity/Wan2.1/generate.py"

@app.post("/generate")
def generate_video(prompt: str = Form(...)):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.mp4"
    output_path = os.path.join(OUTPUT_DIR, filename)

    cmd = [
        "python3", SCRIPT_PATH,
        "--task", "t2v-1.3B",
        "--size", "832*480",
        "--ckpt_dir", MODEL_PATH,
        "--prompt", prompt,
        "--output_path", output_path
    ]

    subprocess.run(cmd, check=True)

    return FileResponse(output_path, media_type="video/mp4", filename=filename)