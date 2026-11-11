import os
from fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from google import genai
from google.genai import types

mcp = FastMCP(
    "GeminiTTS",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    ),
)

client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6J8tBUN_Sj4D7ed42qvKcNTj2gS6BsKU2P1cknS_HTRWg"))

@mcp.tool()
def generate_voice_speech(text_to_speak: str, voice_name: str = "Puck") -> str:
    """Converts user text into spoken voice audio using Gemini 3.8 Flash TTS."""
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash-tts",
            contents=text_to_speak,
            config=types.GenerateContentConfig(
                response_mime_type="audio/mp3",
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                ),
            ),
        )
        return f"Successfully generated speech using voice '{voice_name}' for: {text_to_speak}"
    except Exception as e:
        return f"Error creating audio: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
        stateless_http=True,
    )
