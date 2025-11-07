import streamlit as st
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from groq import Groq
import requests
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import tempfile

# Load environment variables
load_dotenv()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Groq configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ElevenLabs configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Page configuration
st.set_page_config(
    page_title="Outbound Call Demo",
    page_icon="📞",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match React app exactly
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        max-width: 800px !important;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #000000 0%, #333333 100%);
        padding: 30px;
        border-radius: 15px;
        border: 3px solid #e7000b;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .main-header h1 {
        color: #e7000b;
        font-size: 2.8em;
        margin: 0 0 10px 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        color: #ffffff;
        font-size: 1.3em;
        margin: 0;
        opacity: 0.95;
    }
    
    /* Section styling */
    .section-box {
        background: #000000;
        border: 2px solid #e7000b;
        border-radius: 12px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 5px 20px rgba(231, 0, 11, 0.3);
        position: relative;
    }
    
    .section-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: #e7000b;
        border-radius: 12px 0 0 12px;
    }
    
    /* Input styling */
    .stSelectbox > div > div {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #e7000b !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #e7000b !important;
        border-radius: 8px !important;
        padding: 14px !important;
        font-size: 16px !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: transparent !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 0 !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        text-align: center !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #e7000b 0%, #b50009 100%) !important;
        color: #ffffff !important;
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(231, 0, 11, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #000000 0%, #333333 100%) !important;
        border: 2px solid #e7000b !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Phone number list styling */
    .phone-list-item {
        background: #ffffff;
        color: #000000;
        border: 2px solid #e7000b;
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .phone-list-item:hover {
        background: #f8f8f8;
        transform: translateX(8px);
        box-shadow: 0 4px 15px rgba(231, 0, 11, 0.4);
    }
    
    .empty-list {
        text-align: center;
        color: #ffffff;
        font-style: italic;
        font-size: 16px;
        padding: 20px;
    }
    
    /* Status messages */
    .status-message {
        background: #ffffff;
        color: #000000;
        border: 2px solid #e7000b;
        border-radius: 10px;
        padding: 20px;
        margin-top: 25px;
        box-shadow: 0 4px 15px rgba(231, 0, 11, 0.3);
        font-weight: 500;
    }
    
    /* Section headers */
    .section-box h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        margin: 0 0 20px 0 !important;
        padding: 0 !important;
    }
    
    /* Proper spacing for inputs */
    .section-box .stSelectbox,
    .section-box .stTextInput,
    .section-box .stTextArea,
    .section-box .stButton {
        margin-bottom: 0 !important;
    }
    
    /* Column spacing */
    div[data-testid="column"] {
        padding: 0 5px !important;
    }
    
    div[data-testid="column"]:first-child {
        padding-left: 0 !important;
    }
    
    div[data-testid="column"]:last-child {
        padding-right: 0 !important;
    }
    
    /* Hide empty containers */
    div[data-testid="stVerticalBlock"]:empty {
        display: none !important;
    }
    
    div[data-testid="column"]:empty {
        display: none !important;
    }
    
    .element-container:empty {
        display: none !important;
    }
    
    /* Remove all default margins */
    .stMarkdown {
        margin-bottom: 0 !important;
    }
    
    /* Column container styling */
    div[data-testid="column"] {
        background: transparent !important;
    }
    
    /* Hide the horizontal rule/divider */
    hr {
        display: none !important;
    }
    
    /* Remove spacing between sections */
    .row-widget {
        margin: 0 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove top toolbar */
    div[data-testid="stToolbar"] {
        display: none !important;
    }
    
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Hide status container */
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    /* Remove iframe borders */
    iframe {
        border: none !important;
    }
    
    /* Send button special styling */
    .send-all-button button {
        background: #000000 !important;
        color: #ffffff !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        padding: 18px 35px !important;
        width: 100% !important;
        border: 2px solid #e7000b !important;
        border-radius: 10px !important;
        box-shadow: 0 6px 20px rgba(231, 0, 11, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .send-all-button button:hover {
        background: #e7000b !important;
        color: #ffffff !important;
        border: 2px solid #000000 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(231, 0, 11, 0.5) !important;
    }
    
    .send-all-button button:disabled {
        background: #666666 !important;
        color: #cccccc !important;
        cursor: not-allowed !important;
        box-shadow: none !important;
        border: 2px solid #999999 !important;
    }
</style>
""", unsafe_allow_html=True)

# Country codes data (matching React app)
COUNTRY_CODES = [
    {"code": "+91", "country": "India", "flag": "🇮🇳"},
    {"code": "+1", "country": "USA/Canada", "flag": "🇺🇸"},
    {"code": "+44", "country": "UK", "flag": "🇬🇧"},
    {"code": "+61", "country": "Australia", "flag": "🇦🇺"},
    {"code": "+49", "country": "Germany", "flag": "🇩🇪"},
    {"code": "+33", "country": "France", "flag": "🇫🇷"},
    {"code": "+81", "country": "Japan", "flag": "🇯🇵"},
    {"code": "+86", "country": "China", "flag": "🇨🇳"},
    {"code": "+7", "country": "Russia", "flag": "🇷🇺"},
    {"code": "+55", "country": "Brazil", "flag": "🇧🇷"},
    {"code": "+971", "country": "UAE", "flag": "🇦🇪"},
    {"code": "+65", "country": "Singapore", "flag": "🇸🇬"}
]

# Languages with TTS provider info
LANGUAGES = [
    # Indian Languages (ElevenLabs - Multi-lingual support)
    {"code": "en-IN", "name": "English (India)", "flag": "🇮🇳", "voice": "pNInz6obpgDQGcFmaJgB", "provider": "elevenlabs"},  # Adam
    {"code": "hi-IN", "name": "Hindi (हिंदी)", "flag": "🇮🇳", "voice": "pNInz6obpgDQGcFmaJgB", "provider": "elevenlabs"},  # Adam (multi-lingual)
    {"code": "ta-IN", "name": "Tamil (தமிழ்)", "flag": "🇮🇳", "voice": "pNInz6obpgDQGcFmaJgB", "provider": "elevenlabs"},  # Adam (multi-lingual)
    {"code": "te-IN", "name": "Telugu (తెలుగు)", "flag": "🇮🇳", "voice": "pNInz6obpgDQGcFmaJgB", "provider": "elevenlabs"},  # Adam (multi-lingual)
    {"code": "bn-IN", "name": "Bengali (বাংলা)", "flag": "🇮🇳", "voice": "pNInz6obpgDQGcFmaJgB", "provider": "elevenlabs"},  # Adam (multi-lingual)
    {"code": "mr-IN", "name": "Marathi (मराठी)", "flag": "🇮🇳", "voice": "pNInz6obpgDQGcFmaJgB", "provider": "elevenlabs"},  # Adam (multi-lingual)
    {"code": "gu-IN", "name": "Gujarati (ગુજરાતી)", "flag": "🇮🇳", "voice": "pNInz6obpgDQGcFmaJgB", "provider": "elevenlabs"},  # Adam (multi-lingual)
    {"code": "kn-IN", "name": "Kannada (ಕನ್ನಡ)", "flag": "🇮🇳", "voice": "pNInz6obpgDQGcFmaJgB", "provider": "elevenlabs"},  # Adam (multi-lingual)
    {"code": "ml-IN", "name": "Malayalam (മലയാളം)", "flag": "🇮🇳", "voice": "pNInz6obpgDQGcFmaJgB", "provider": "elevenlabs"},  # Adam (multi-lingual)
    
    # International Languages (Twilio Polly)
    {"code": "en-US", "name": "English (US)", "flag": "🇺🇸", "voice": "alice", "provider": "twilio"},
    {"code": "en-GB", "name": "English (UK)", "flag": "🇬🇧", "voice": "Polly.Amy", "provider": "twilio"},
    {"code": "es-ES", "name": "Spanish (Español)", "flag": "🇪🇸", "voice": "Polly.Conchita", "provider": "twilio"},
    {"code": "fr-FR", "name": "French (Français)", "flag": "🇫🇷", "voice": "Polly.Celine", "provider": "twilio"},
    {"code": "de-DE", "name": "German (Deutsch)", "flag": "🇩🇪", "voice": "Polly.Marlene", "provider": "twilio"},
    {"code": "pt-BR", "name": "Portuguese (Brazil)", "flag": "🇧🇷", "voice": "Polly.Vitoria", "provider": "twilio"}
]

# Function to translate text using Groq
def translate_text_groq(text, target_language):
    try:
        if not GROQ_API_KEY:
            return text  # Return original if no API key
        
        client = Groq(api_key=GROQ_API_KEY)
        
        # Language mapping for better translation prompts
        language_names = {
            "en-IN": "English",
            "hi-IN": "Hindi",
            "ta-IN": "Tamil",
            "te-IN": "Telugu",
            "bn-IN": "Bengali",
            "mr-IN": "Marathi",
            "gu-IN": "Gujarati",
            "kn-IN": "Kannada",
            "ml-IN": "Malayalam",
            "en-US": "English",
            "en-GB": "English",
            "es-ES": "Spanish",
            "fr-FR": "French",
            "de-DE": "German",
            "pt-BR": "Portuguese"
        }
        
        target_lang_name = language_names.get(target_language, "English")
        
        # Skip translation if already in English
        if target_lang_name == "English":
            return text
        
        # Use Groq's Whisper model for translation
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional translator. Translate the following text to {target_lang_name}. Only provide the translation, no explanations."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            model="llama-3.3-70b-versatile",  # Using Groq's powerful model
            temperature=0.3,
            max_tokens=1024
        )
        
        translated_text = chat_completion.choices[0].message.content.strip()
        return translated_text
        
    except Exception as e:
        st.warning(f"Translation failed: {str(e)}. Using original text.")
        return text

# Function to generate speech using ElevenLabs TTS
def generate_elevenlabs_tts(text, voice_id):
    try:
        if not ELEVENLABS_API_KEY:
            return None
        
        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        # Generate speech
        response = client.text_to_speech.convert(
            voice_id=voice_id,
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_multilingual_v2",  # Supports 29 languages including Indian languages
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True,
            ),
        )
        
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            for chunk in response:
                if chunk:
                    temp_audio.write(chunk)
            return temp_audio.name
            
    except Exception as e:
        st.warning(f"ElevenLabs TTS failed: {str(e)}. Falling back to Twilio.")
        return None

# Function to upload audio to tmpfiles.org (more reliable temporary hosting)
def upload_audio_to_tmpfiles(audio_file_path):
    try:
        with open(audio_file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    # tmpfiles.org returns URL like: https://tmpfiles.org/12345
                    # We need to convert it to direct download: https://tmpfiles.org/dl/12345
                    url = data.get('data', {}).get('url', '')
                    if url:
                        # Convert to direct download URL
                        direct_url = url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
                        return direct_url
        return None
    except Exception as e:
        st.warning(f"Audio upload failed: {str(e)}")
        return None

# Function to make Twilio call with multi-lingual support
def make_twilio_call(to_number, message, language_code="en-IN", voice="alice", provider="twilio"):
    try:
        # Initialize Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        if provider == "elevenlabs":
            # Check if we have cached audio URL
            if st.session_state.cached_audio_url:
                # Use cached audio
                twiml = VoiceResponse()
                twiml.play(st.session_state.cached_audio_url)
            else:
                # Generate new audio
                audio_file = generate_elevenlabs_tts(message, voice)
                
                if audio_file:
                    # Upload audio to temporary hosting
                    audio_url = upload_audio_to_tmpfiles(audio_file)
                    
                    if audio_url:
                        # Cache the URL
                        st.session_state.cached_audio_url = audio_url
                        st.session_state.cached_audio_file = audio_file
                        
                        # Create TwiML with audio playback
                        twiml = VoiceResponse()
                        twiml.play(audio_url)
                    else:
                        # Fallback to Twilio TTS if upload fails
                        st.warning("Audio upload failed. Using Twilio TTS fallback.")
                        twiml = VoiceResponse()
                        twiml.say(message, language=language_code)
                else:
                    # Fallback to Twilio TTS
                    twiml = VoiceResponse()
                    twiml.say(message, language=language_code)
        else:
            # Use Twilio Polly voices
            twiml = VoiceResponse()
            twiml.say(message, voice=voice, language=language_code)
        
        # Make the call
        call = client.calls.create(
            to=to_number,
            from_=TWILIO_PHONE_NUMBER,
            twiml=str(twiml)
        )
        
        return {
            "success": True, 
            "sid": call.sid, 
            "status": call.status,
            "to": to_number,
            "from": TWILIO_PHONE_NUMBER
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# Initialize session state
if 'phone_numbers' not in st.session_state:
    st.session_state.phone_numbers = []
if 'status_message' not in st.session_state:
    st.session_state.status_message = ""
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "en-IN"
if 'translated_message' not in st.session_state:
    st.session_state.translated_message = ""
if 'cached_audio_file' not in st.session_state:
    st.session_state.cached_audio_file = None
if 'cached_audio_url' not in st.session_state:
    st.session_state.cached_audio_url = None

# Main app
def main():
    # Header (matching React app exactly)
    st.markdown("""
    <div class="main-header">
        <h1>Outbound Call Demo</h1>
        <p>Automated Reminder System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 1: Add Customer Phone Numbers
    with st.container():
        st.markdown('<div class="section-box"><h3>1. Add Customer Phone Numbers</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2.5, 4, 1.5])
        
        with col1:
            # Country code dropdown
            country_options = [f"{c['flag']} {c['code']} {c['country']}" for c in COUNTRY_CODES]
            selected_country = st.selectbox(
                "Country Code",
                options=country_options,
                index=0,  # Default to India
                label_visibility="collapsed",
                key="country_select"
            )
            # Extract country code
            country_code = selected_country.split()[1]  # Gets "+91" from "🇮🇳 +91 India"
        
        with col2:
            phone_number = st.text_input(
                "Phone Number",
                placeholder="Enter 10-digit number",
                max_chars=10,
                label_visibility="collapsed",
                key="phone_input"
            )
        
        with col3:
            if st.button("Add to List", use_container_width=True, key="add_btn"):
                if phone_number and len(phone_number) == 10 and phone_number.isdigit():
                    full_number = f"{country_code}{phone_number}"
                    if full_number not in st.session_state.phone_numbers:
                        st.session_state.phone_numbers.append(full_number)
                        st.session_state.status_message = ""
                        st.rerun()
                    else:
                        st.session_state.status_message = f"Number {full_number} is already in the list."
                else:
                    st.session_state.status_message = "Please enter a valid 10-digit phone number."
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Calling List Section
    with st.container():
        st.markdown('<div class="section-box"><h3>Calling List</h3>', unsafe_allow_html=True)
        
        if len(st.session_state.phone_numbers) == 0:
            st.markdown('<p class="empty-list">No numbers added yet.</p>', unsafe_allow_html=True)
        else:
            for i, number in enumerate(st.session_state.phone_numbers):
                col1, col2 = st.columns([6, 1])
                with col1:
                    st.markdown(f'<div class="phone-list-item">{number}</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("×", key=f"remove_{i}", help="Remove number"):
                        st.session_state.phone_numbers.remove(number)
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Select Language
    with st.container():
        st.markdown('<div class="section-box"><h3>2. Select Language for Call</h3>', unsafe_allow_html=True)
        
        language_options = [f"{lang['flag']} {lang['name']}" for lang in LANGUAGES]
        selected_language_display = st.selectbox(
            "Language",
            options=language_options,
            index=0,  # Default to English (India)
            label_visibility="collapsed",
            key="language_select"
        )
        
        # Extract language code
        selected_lang_index = language_options.index(selected_language_display)
        st.session_state.selected_language = LANGUAGES[selected_lang_index]["code"]
        selected_voice = LANGUAGES[selected_lang_index]["voice"]
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3: Review Reminder Message
    with st.container():
        st.markdown('<div class="section-box"><h3>3. Review Reminder Message</h3>', unsafe_allow_html=True)
        
        default_message = (
            "Hello, this is an automated payment reminder from Prime Financial Bank. "
            "Your loan account number PF123456789 has an upcoming EMI payment due on 15th November 2025. "
            "The EMI amount is Rupees 25,000. Your outstanding loan balance is Rupees 4,50,000. "
            "Please ensure the payment is made on or before the due date to avoid late payment charges of Rupees 500 "
            "and impact on your credit score. You can make the payment through our mobile app, internet banking, "
            "or visit the nearest branch. For any queries, please call our customer care at 1800-555-0123. "
            "Thank you for banking with Prime Financial Bank."
        )
        
        message = st.text_area(
            "Message",
            value=default_message,
            height=140,
            label_visibility="collapsed",
            key="message_input"
        )
        
        # Translate and Generate Audio buttons
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("🌐 Translate", use_container_width=True, key="translate_btn"):
                with st.spinner("Translating..."):
                    st.session_state.translated_message = translate_text_groq(
                        message, 
                        st.session_state.selected_language
                    )
                    # Clear cached audio when translating
                    st.session_state.cached_audio_url = None
                    st.session_state.cached_audio_file = None
                    st.rerun()
        
        with col3:
            # Show generate audio button for ElevenLabs languages
            selected_lang_obj = next((l for l in LANGUAGES if l["code"] == st.session_state.selected_language), None)
            if selected_lang_obj and selected_lang_obj["provider"] == "elevenlabs":
                if st.button("🎙️ Generate Audio", use_container_width=True, key="generate_audio_btn"):
                    with st.spinner("Generating audio..."):
                        final_msg = st.session_state.translated_message if st.session_state.translated_message else message
                        audio_file = generate_elevenlabs_tts(final_msg, selected_lang_obj["voice"])
                        
                        if audio_file:
                            audio_url = upload_audio_to_tmpfiles(audio_file)
                            if audio_url:
                                st.session_state.cached_audio_url = audio_url
                                st.session_state.cached_audio_file = audio_file
                                st.success("✅ Audio generated and cached!")
                                
                                # Show audio player
                                with open(audio_file, 'rb') as f:
                                    st.audio(f.read(), format='audio/mp3')
                            else:
                                st.error("Failed to upload audio")
                        else:
                            st.error("Failed to generate audio")
        
        # Show translated message if available
        if st.session_state.translated_message and st.session_state.selected_language != "en-IN":
            st.markdown("**Translated Message:**")
            st.text_area(
                "Translated",
                value=st.session_state.translated_message,
                height=140,
                label_visibility="collapsed",
                key="translated_display",
                disabled=True
            )
        
        # Show cached audio status
        if st.session_state.cached_audio_url:
            st.success("✅ Audio ready for calls!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 4: Send All Reminders
    st.markdown('<div class="send-all-button" style="margin: 30px 0;">', unsafe_allow_html=True)
    
    send_button = st.button(
        "SEND ALL REMINDERS",
        disabled=(len(st.session_state.phone_numbers) == 0),
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if send_button:
            if len(st.session_state.phone_numbers) == 0:
                st.session_state.status_message = "Please add at least one phone number to the list."
            else:
                st.session_state.status_message = "Initiating calls... Please wait."
                
                # Use translated message if available, otherwise original
                final_message = st.session_state.translated_message if st.session_state.translated_message else message
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                call_results = []
                total_numbers = len(st.session_state.phone_numbers)
                
                for i, number in enumerate(st.session_state.phone_numbers):
                    # Update progress
                    progress = (i + 1) / total_numbers
                    progress_bar.progress(progress)
                    status_text.text(f"Calling {number}... ({i+1}/{total_numbers})")
                    
                    # Extract just the phone number (remove country code for API)
                    if number.startswith('+91'):
                        api_number = number[3:]  # Remove +91
                    elif number.startswith('+1'):
                        api_number = number[2:]  # Remove +1
                    else:
                        # For other country codes, remove the + and country code
                        import re
                        match = re.match(r'^\+\d{1,4}(.+)$', number)
                        api_number = match.group(1) if match else number
                    
                    # Make the call with selected language
                    # Get provider info
                    selected_lang_obj = next((l for l in LANGUAGES if l["code"] == st.session_state.selected_language), None)
                    provider = selected_lang_obj["provider"] if selected_lang_obj else "twilio"
                    
                    result = make_twilio_call(
                        f"+91{api_number}", 
                        final_message,
                        st.session_state.selected_language,
                        selected_voice,
                        provider
                    )
                    call_results.append({"number": number, "result": result})
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Show results
                successful_calls = sum(1 for r in call_results if r["result"]["success"])
                failed_calls = total_numbers - successful_calls
                
                st.session_state.status_message = f"✅ Successfully initiated calls to {successful_calls} numbers."
                
                # Clear the list after sending
                st.session_state.phone_numbers = []
                st.rerun()
    
    # Status message
    if st.session_state.status_message:
        st.markdown(f'<div class="status-message"><p>{st.session_state.status_message}</p></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
