import os
import sys
import time
import json
import requests
import subprocess
from gradio_client import Client

ENV_CONFIG = {
    "character_desc": os.getenv("INPUT_CHARACTER", "An old pirate with a silver cybernetic eye and white beard"),
    "scene_1_action": os.getenv("INPUT_SCENE_1", "sitting in a dark tavern drinking glowing blue neon juice"),
    "scene_2_action": os.getenv("INPUT_SCENE_2", "running away from explosions down a wet narrow street"),
    "camera_s1": os.getenv("INPUT_CAMERA_1", "Slow tracking shot from left to right"),
    "camera_s2": os.getenv("INPUT_CAMERA_2", "Dramatic cinematic low-angle handheld camera movement")
}

def generate_google_flow_takar_video(char_core, action_prompt, motion, scene_id):
    print(f"🎬 [FLOW ENGINE NODE - SCENE {scene_id}]: Mapping character mesh definitions...")
    master_cinematic_prompt = f"Cinematic shot of {char_core}, {action_prompt}. Camera dynamics: {motion}. Photorealistic, ultra-detailed textures, 8k render, perfect character identity tracking."
    
    # FIX: Live server nodes space configuration path mappings
    # If the primary channel is overloaded, it automatically switches to alternative clusters
    spaces_cluster_pool = [
        "Qadeer24/Wan-AI-Wan2.1-T2V-14B",
        "fffiloni/Wan2.1"
    ]
    
    target_space = spaces_cluster_pool[0] if scene_id == 1 else spaces_cluster_pool[1]
    
    for attempt in range(len(spaces_cluster_pool)):
        try:
            print(f"📡 Handshaking with cluster endpoint node: {target_space}...")
            client = Client(target_space)
            
            # Universal parameter execution framework mapping
            result = client.predict(
                prompt=master_cinematic_prompt,
                negative_prompt="deformed body, face shift, blurry eyes, flashing artifacts, text overlay, low-end render",
                api_name="/generate_video"
            )
            
            output_clip_path = f"raw_scene_block_{scene_id}.mp4"
            if os.path.exists(output_clip_path):
                os.remove(output_clip_path)
            os.rename(result, output_clip_path)
            print(f"✅ [NODE SUCCESS]: Scene {scene_id} generated perfectly via {target_space}!")
            return output_clip_path
            
        except Exception as e:
            print(f"⚠️ Channel {target_space} busy or failed: {str(e)}")
            # Alternate recovery backup path assignment
            target_space = spaces_cluster_pool[(attempt + 1) % len(spaces_cluster_pool)]
            time.sleep(5)
            
    print("❌ [CRITICAL PIPELINE BREAK]: All public open-source server networks are currently full.")
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
    clip1 = generate_google_flow_takar_video(ENV_CONFIG["character_desc"], ENV_CONFIG["scene_1_action"], ENV_CONFIG["camera_s1"], 1)
    clip2 = generate_google_flow_takar_video(ENV_CONFIG["character_desc"], ENV_CONFIG["scene_2_action"], ENV_CONFIG["camera_s2"], 2)
    compile_master_cinema(clip1, clip2)
