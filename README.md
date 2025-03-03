# FastRTC Multilingual Chat

A real-time multilingual chat application using **FastRTC, Whisper STT, Google Cloud TTS, and Translate APIs**.

## Features
✅ Real-time **speech recognition** (STT) using Whisper  
✅ **Automatic translation** using Google Cloud Translate  
✅ **Natural-sounding speech synthesis** (TTS) using Google Cloud  
✅ **Supports Latin American Spanish (es-US)**  

## Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/intisoto-ai/fastrtc-chat.git
cd fastrtc-chat
```

### 2️⃣ Set Up Virtual Environment (Anaconda)
```sh
conda create --name fastrtc-chat python=3.11
conda activate fastrtc-chat
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Google Cloud API Keys
- Create a **Google Cloud Service Account**.
- Enable **Text-to-Speech** and **Translate APIs**.
- Download your JSON key and set:
```sh
export GOOGLE_FASTRTC_KEY="path/to/your/google-key.json"
```

## Running the App
```sh
python fastrtc_chat/app.py
```

## Contribution Guidelines
We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Added new feature"`).
4. Push to your branch (`git push origin feature-name`).
5. Open a **Pull Request**.

## License
This project is licensed under the MIT License.

## Support
If you like this app, consider supporting me:

<a href="https://www.buymeacoffee.com/intisoto" target="_blank">
    <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=intisoto&button_colour=FFDD00&font_colour=000000&font_family=Arial&outline_colour=000000&coffee_colour=ffffff" 
    alt="Buy Me A Coffee" width="200">
</a>