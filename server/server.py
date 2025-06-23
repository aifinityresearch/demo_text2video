from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
import subprocess
import time
import os
import glob

app = FastAPI()
OUTPUT_DIR = "/home/aifinity/Wan2.1/demo_text2video/outputs"
MODEL_PATH = "/home/aifinity/Wan2.1/models/Wan2.1-T2V-1.3B"
SCRIPT_PATH = "/home/aifinity/Wan2.1/generate.py"
OUTPUT_DIR = os.getcwd()


@app.post("/generate")
def generate_video(prompt: str = Form(...)):
    print(f"[INFO] Received prompt: {prompt}")
 ## os.makedirs(OUTPUT_DIR, exist_ok=True)  # Create the folder if it doesn't exist
    # Capture baseline file list before generation
    existing_files = set(os.listdir(OUTPUT_DIR))
  
    cmd = [
        "python3", SCRIPT_PATH,
        "--task", "t2v-1.3B",
        "--size", "832*480",
        "--ckpt_dir", MODEL_PATH,
        "--prompt", prompt
        # ⛔️ Removed --output_path
    ]

    print(f"[INFO] Running command: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Generation failed with return code {e.returncode}")
        return JSONResponse(status_code=500, content={"error": f"Script failed: {e}"})
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

    # 🕵️ Find newly created video file
    new_files = set(os.listdir(OUTPUT_DIR)) - existing_files
    mp4_candidates = [f for f in new_files if f.endswith(".mp4")]

    if not mp4_candidates:
        print("[ERROR] No .mp4 file was created.")
        return JSONResponse(status_code=500, content={"error": "Video generation failed. No .mp4 output found."})

    # Grab the newest file (just in case)
    full_paths = [os.path.join(OUTPUT_DIR, f) for f in mp4_candidates]
    latest_file = max(full_paths, key=os.path.getctime)

    print(f"[SUCCESS] Returning video file: {latest_file}")
    return FileResponse(latest_file, media_type="video/mp4", filename=os.path.basename(latest_file))
