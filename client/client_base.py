import requests
import time

# === Config ===
API_URL = "http://13.203.204.63:7860/generate"  # Replace with your EC2 IP
prompt = "A futuristic drone flying over a canyon at sunset"  # <-- Hardcoded prompt

def generate(prompt):
    print("[DEBUG] Using prompt:", prompt)

    try:
        print("[DEBUG] Sending POST request to:", API_URL)
        start_time = time.time()

        response = requests.post(API_URL, data={"prompt": prompt}, timeout=3000)

        duration = time.time() - start_time
        print(f"[DEBUG] Response status code: {response.status_code}")
        print(f"[DEBUG] Generation took {duration:.2f} seconds")

        if response.status_code == 200:
            file_path = "result.mp4"
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"[DEBUG] Video saved successfully as '{file_path}'")
        else:
            print("[ERROR] Server responded with error:", response.text)

    except Exception as e:
        print("[EXCEPTION] Request failed:", e)

# === Run ===
generate(prompt)
