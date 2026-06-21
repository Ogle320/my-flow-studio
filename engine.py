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
    print(f"🎬 [FLOW ENGINE NODE - SCENE {scene_id}]: Generating realistic cinematic video tracking layers...")
    master_cinematic_prompt = f"Cinematic shot of {char_core}, {action_prompt}. Camera dynamics: {motion}. Photorealistic, ultra-detailed textures, 8k render, master composition."
    
    url = "https://fal.run"
    headers = {
        "Authorization": f"Key {FAL_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": master_cinematic_prompt,
        "aspect_ratio": "16:9",
        "num_frames": 81 # Standard premium 5-second fluid output frame block
    }
    
    try:
        # Step 1: Submit generation job to queue
        response = requests.post(url, json=payload, headers=headers)
        request_id = response.json().get("request_id")
        
        # Step 2: Loop monitor status check until completion
        status_url = f"https://fal.run/requests/{request_id}"
        print("⏳ Processing inside high-end dedicated GPU cluster nodes...")
        
        for attempt in range(40):
            check_status = requests.get(status_url, headers=headers).json()
            if check_status.get("status") == "COMPLETED":
                # Download raw video link natively
                video_url = check_status['logs'][-1] if 'video' not in check_status else check_status['video']['url']
                video_bytes = requests.get(video_url).content
                
                output_clip_path = f"raw_scene_block_{scene_id}.mp4"
                with open(output_clip_path, "wb") as f:
                    f.write(video_bytes)
                print(f"✅ [NODE SUCCESS]: Scene {scene_id} rendered perfectly!")
                return output_clip_path
            time.sleep(5)
            
        raise Exception("Cloud Render Timed out on public node queue limits.")
    except Exception as e:
        print(f"❌ Engine critical block crash: {str(e)}")
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
        print("❌ CRITICAL ERROR: FAL_KEY missing from Repository Secrets Configuration!")
        sys.exit(1)
        
    clip1 = render_fal_premium_video(ENV_CONFIG["character_desc"], ENV_CONFIG["scene_1_action"], ENV_CONFIG["camera_s1"], 1)
    clip2 = render_fal_premium_video(ENV_CONFIG["character_desc"], ENV_CONFIG["scene_2_action"], ENV_CONFIG["camera_s2"], 2)
    compile_master_cinema(clip1, clip2)
