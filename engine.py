import os
import sys
import time
import requests
import subprocess

ENV_CONFIG = {
    "character_desc": os.getenv("INPUT_CHARACTER", "An old pirate with a silver cybernetic eye and white beard"),
    "scene_1_action": os.getenv("INPUT_SCENE_1", "sitting in a dark tavern drinking glowing blue neon juice"),
    "scene_2_action": os.getenv("INPUT_SCENE_2", "running away from explosions down a wet narrow street"),
    "camera_s1": os.getenv("INPUT_CAMERA_1", "Slow tracking shot from left to right"),
    "camera_s2": os.getenv("INPUT_CAMERA_2", "Dramatic cinematic low-angle handheld camera movement")
}

FAL_KEY = os.getenv("FAL_KEY")

def render_fal_premium_video(char_core, action_prompt, motion, scene_id):
    print(f"🎬 [FLOW ENGINE NODE - SCENE {scene_id}]: Building cinematic frames matrix...")
    master_cinematic_prompt = f"Cinematic shot of {char_core}, {action_prompt}. Camera dynamics: {motion}. Photorealistic, ultra-detailed textures, 8k render, masterpiece composition."
    
    # Hardcoded absolute URLs to prevent any string connection errors
    submit_url = "https://fal.run"
    
    headers = {
        "Authorization": f"Key {FAL_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "prompt": master_cinematic_prompt,
            "aspect_ratio": "16:9"
        }
    }
    
    try:
        print(f"📡 Dispatching data payload to gateway server link: {submit_url}")
        response = requests.post(submit_url, json=payload, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Queue handshake rejected with code {response.status_code}: {response.text}")
            sys.exit(1)
            
        res_data = response.json()
        request_id = res_data.get("request_id")
        
        if not request_id:
            print(f"❌ Structural map error: Valid tracking request_id token not found. Raw: {res_data}")
            sys.exit(1)
            
        status_url = f"https://fal.run/requests/{request_id}"
        print(f"⏳ Tracking Job Token: [{request_id}]. Processing inside H100 cloud nodes...")
        
        for attempt in range(60): # 5 minutes maximum runtime tracking checks
            status_response = requests.get(status_url, headers=headers)
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                current_state = status_data.get("status")
                
                if current_state == "COMPLETED":
                    video_url = None
                    if "video" in status_data and "url" in status_data["video"]:
                        video_url = status_data["video"]["url"]
                    elif "outputs" in status_data and "video" in status_data["outputs"]:
                        video_url = status_data["outputs"]["video"].get("url")
                    elif "video" in status_data.get("output", {}):
                        video_url = status_data["output"]["video"].get("url")
                        
                    if not video_url:
                        print(f"❌ Video payload links array empty inside output structural elements: {status_data}")
                        sys.exit(1)
                        
                    print(f"📥 Downloading raw cinematic video array stream from source chunk cluster...")
                    video_bytes = requests.get(video_url).content
                    
                    output_clip_path = f"raw_scene_block_{scene_id}.mp4"
                    if os.path.exists(output_clip_path):
                        os.remove(output_clip_path)
                        
                    with open(output_clip_path, "wb") as f:
                        f.write(video_bytes)
                        
                    print(f"✅ [NODE SUCCESS]: Scene {scene_id} generated perfectly!")
                    return output_clip_path
                    
                elif current_state == "FAILED":
                    print(f"❌ Processing pipeline failed inside the server node architecture layout: {status_data}")
                    sys.exit(1)
                    
            time.sleep(5)
            
        print("❌ [TIMEOUT ERROR]: Generation task hung beyond loop limit bounds.")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Exception logic mapping block execution failure: {str(e)}")
        sys.exit(1)

def compile_master_cinema(s1_file, s2_file):
    print("📦 [MASTER ASSEMBLER]: Initiating native multi-clip formatting layers...")
    consolidated_output = "flow_studio_masterpiece_1080p.mp4"
    
    with open("production_stitching_list.txt", "w") as manifest:
        manifest.write(f"file '{s1_file}'\n")
        manifest.write(f"file '{s2_file}'\n")
        
    try:
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
            "-i", "production_stitching_list.txt", "-c", "copy", consolidated_output
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        subprocess.run([
            "ffmpeg", "-y", "-i", consolidated_output, "-ss", "00:00:02", "-vframes", "1", "production_poster_preview.png"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("🚀 [MASTER PROCESS DONE]: Movie compilation successfully completed. Assets frozen!")
    except Exception as e:
        print(f"⚠️ Compiler packaging failure alert: {str(e)}")

if __name__ == "__main__":
    if not FAL_KEY:
        print("❌ CRITICAL ERROR: FAL_KEY variable missing from Repository Secrets config panel!")
        sys.exit(1)
        
    clip1 = render_fal_premium_video(ENV_CONFIG["character_desc"], ENV_CONFIG["scene_1_action"], ENV_CONFIG["camera_s1"], 1)
    clip2 = render_fal_premium_video(ENV_CONFIG["character_desc"], ENV_CONFIG["scene_2_action"], ENV_CONFIG["camera_s2"], 2)
    compile_master_cinema(clip1, clip2)
