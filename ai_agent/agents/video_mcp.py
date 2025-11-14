
import json
from pydantic import BaseModel, Field
from google import genai
from google.genai.types import HttpOptions, Part

class VideoAnalysis(BaseModel):
    video_url: str = Field(description="URL of the video")
    mood: str = Field(description="Overall mood of the video")
    insights: str = Field(description="Key insights from the video content")
    storyline: list = Field(default=[], description="Storyline breakdown of the video")
    colors: list = Field(default=[], description="Dominant colors in the video")

def analyze_video_with_gemini(video_url: str, project: str | None, location: str = "us-central1"):
    try:
        client = genai.Client(vertexai=True, project=project, location=location, http_options=HttpOptions(api_version="v1"))
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=[
                Part.from_uri(file_uri=video_url, mime_type="video/mp4"),
                {"text": "한국어로 분석. JSON으로.", "videoMetadata": {"startOffset": "0s"}}
            ],
            config={
                "response_mime_type": "application/json",
                "response_schema": VideoAnalysis,
                "temperature": 0
            }
        )
        return json.loads(response.text)
    except Exception as e:
        return {
            "video_url": "",
            "mood": "",
            "insights": "",
            "storyline": [],
            "colors": [],
        }
