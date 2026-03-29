import os
import time
import requests
import json

# ==========================================
# CONFIGURATION - ENTER YOUR API KEYS HERE
# ==========================================
SHOTSTACK_KEY = "n9gHnmjTYDF9uz6GqEXjxhDwSAKq9EfHPUBCJqox"
ELEVENLABS_KEY = "sk_77f0969c0036e368f82ff47f7331ec8a2497999773e18f9d"

# GitHub Base URL for Assets
GITHUB_USER = "Siva2109"
REPO_NAME = "sivadelight-repo"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/master/youtube_assets/"

# Assets and Script paths
ASSETS_DIR = "/home/staycool21/AntiGravity/SivaDelight_Final/YouTube_Assets"
SCRIPT_FILE = os.path.join(ASSETS_DIR, "youtube_script.md")
AUDIO_OUTPUT = os.path.join(ASSETS_DIR, "voiceover.mp3")

# Scene Image Files mapping (Script scenes to images)
SCENES = [
    {"img": "sivadelight_youtube_intro_1773734712879.png", "duration": 8},
    {"img": "kodi_prerequisites_visual_1773734746201.png", "duration": 12},
    {"img": "kodi_add_source_visual_1773734780085.png", "duration": 15},
    {"img": "kodi_install_steps_visual_1773734813440.png", "duration": 20},
    {"img": "sivadelight_youtube_outro_1773734879777.png", "duration": 10}
]

def generate_voiceover(text):
    print("Generating voiceover with ElevenLabs...")
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_KEY}
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}}
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open(AUDIO_OUTPUT, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"ElevenLabs Error {response.status_code}: {response.text}")
    return False

def render_video():
    print("Rendering video with Shotstack...")
    shotstack_url = "https://api.shotstack.io/stage/render"
    headers = {"Content-Type": "application/json", "x-api-key": SHOTSTACK_KEY}

    clips = []
    start = 0
    for scene in SCENES:
        clip = {
            "asset": {"type": "image", "src": BASE_URL + scene["img"]},
            "start": start,
            "length": scene["duration"],
            "transition": {"in": "fade", "out": "fade"}
        }
        clips.append(clip)
        start += scene["duration"]

    # Simple background music or audio track would be added here
    # In this version, we combine the images. Syncing with the specific MP3 generated
    # would involve measuring the MP3 length and distributing scene durations.

    # Shotstack JSON structure for the video
    total_duration = start
    data = {
        "timeline": {
            "background": "#000000",
            "tracks": [
                {"clips": clips},
                {
                    "clips": [
                        {
                            "asset": {"type": "audio", "src": BASE_URL + "voiceover.mp3"},
                            "start": 0,
                            "length": total_duration
                        }
                    ]
                }
            ]
        },
        "output": {"format": "mp4", "resolution": "hd"}
    }

    response = requests.post(shotstack_url, json=data, headers=headers)
    if response.status_code == 201:
        render_id = response.json()["response"]["id"]
        print(f"Render started! ID: {render_id}")
        return render_id
    else:
        print(f"Shotstack Error {response.status_code}: {response.text}")
    return None

if __name__ == "__main__":
    if SHOTSTACK_KEY == "PASTE_YOUR_SHOTSTACK_KEY_HERE" or ELEVENLABS_KEY == "PASTE_YOUR_ELEVENLABS_KEY_HERE":
        print("Please enter your API keys in the script first!")
    else:
        with open(SCRIPT_FILE, 'r') as f:
            full_script = f.read()
        clean_text = "\n".join([line for line in full_script.split("\n") if not line.startswith("#") and line.strip()])
        
        if not os.path.exists(AUDIO_OUTPUT):
            if not generate_voiceover(clean_text):
                print("Failed to generate voiceover. Exiting.")
                exit(1)
        else:
            print("Using existing voiceover.mp3 to save credits.")
        
        render_id = render_video()
        if render_id:
            print(f"Check status at: https://api.shotstack.io/stage/render/{render_id}")
