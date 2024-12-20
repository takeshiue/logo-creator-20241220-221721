import os
import logging
import requests
import uuid
from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default-secret-key")

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Ensure the cache directory exists
CACHE_DIR = os.path.join(app.static_folder, 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        prompt = request.json.get('prompt')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        # Generate image using DALL-E 3
        system_prompt = """
ユーザープロンプトに基づいて、白黒のイラストを描いてください。
条件は以下の通りです。
-キャンバスの80%のサイズの円を中央に描き、その中にイラストを描いてください。
-円の外周には絵を描かないでください
-背景は透明にして下さい
-イラストは比較的簡易なイラストとしあまり複雑なものにしないでください。
-イラストは白黒で、シンプルな線画スタイルにしてください。
"""
        enhanced_prompt = f"{system_prompt}\nユーザーのリクエスト: {prompt}"
        
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            n=1,
            size="1024x1024",
            style="vivid"
        )

        # Download and cache the image
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            raise Exception("Failed to download image from OpenAI")

        # Save the image with a unique filename
        filename = f"{uuid.uuid4()}.png"
        cache_path = os.path.join(CACHE_DIR, filename)
        
        with open(cache_path, 'wb') as f:
            f.write(image_response.content)

        # Return the cached image URL
        cached_url = f"/static/cache/{filename}"
        return jsonify({'url': cached_url})
    except Exception as e:
        logging.error(f"Error generating image: {str(e)}")
        return jsonify({'error': str(e)}), 500
