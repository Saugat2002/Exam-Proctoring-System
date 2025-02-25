from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
import os
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
from .audio.audio_report import *
from .audio.utils.text_utils import generate_report
from .audio.scripts.speaker_diarization import initialize_model, diarized_transcription
from .audio.scripts.asr_transcribe import initialize_asr_pipeline
from .audio.utils import audio_utils
from manage import base_dir
from dashboard.models import Student

def perform_diarized_transcription(finetuned_pipeline, audio_file, output_file, asr_pipeline):
    try:
        diarized_transcription(finetuned_pipeline, audio_file, output_file, asr_pipeline)
    except Exception as e:
        print(f"An error occurred during diarized transcription: {e}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "audio/model","segmentation.ckpt")
HUGGINGFACE_TOKEN = "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"
AUDIO_FILE = os.path.join(BASE_DIR, "audio/data/audio_files","output_audio.wav")#"webapp/audio/data/audio_files/output_audio.wav"
EVIDENCE_FILE = os.path.join(BASE_DIR, "audio/data/evidence","evidence.txt")
REPORT_FILE = os.path.join(BASE_DIR, "audio/data/report","report.txt")
KEYWORDS_FILE = os.path.join(BASE_DIR, "audio/utils","cheating_keywords.txt")

# Create your views here.
# def get_audio_report(request):

#     audio_utils.extract_wav_from_mp4(VIDEO_FILE, AUDIO_FILE)

#     try:
#         diarization_pipeline = initialize_model(MODEL_PATH, HUGGINGFACE_TOKEN)
#         asr_pipeline = initialize_asr_pipeline(model_id="lord-reso/whisper-small-inbrowser-proctor")
#     except Exception as e:
#         print(f"An error occurred during initialization: {e}")
#         return

#     perform_diarized_transcription(diarization_pipeline, AUDIO_FILE, EVIDENCE_FILE, asr_pipeline)

#     try:
#         with open(EVIDENCE_FILE, 'r') as file:
#             transcription = file.read()
#         generate_report(transcription, KEYWORDS_FILE, REPORT_FILE)
#     except Exception as e:
#         print(f"An error occurred during report generation: {e}")
#     transcripts = read_transcript(EVIDENCE_FILE)
#     keywords = read_cheating_keywords(REPORT_FILE)

#     fig = make_subplots(
#         rows=2,
#         cols=1,
#         subplot_titles=("Transcript Timeline", "Top 5 Cheating Keywords"),
#         specs=[[{"type": "xy"}], [{"type": "domain"}]],
#         vertical_spacing=0.3
#     )
#     create_timeline(fig, transcripts)
#     create_pie_chart(fig, keywords)

#     fig.update_layout(
#     height=1250, 
#     showlegend=False,
#     title_text="Transcript Timeline Visualization",  
#     title_x=0.5, 
#     title_font=dict(size=24)
#     )
#     plot(fig, filename=f'{BASE_DIR}/templates/audio_report.html')
#     print("Audio report generated successfully")

#     return HttpResponse("Audio report generated successfully")


def get_audio_report(request, id):
    try:
        student = Student.objects.get(id=id)
        email = student.email.replace("@","")
        VIDEO_FILE = os.path.join(base_dir, "backend", "media", "proctoring_videos",f"{email}_recording.mp4")  
        audio_utils.extract_wav_from_mp4(VIDEO_FILE, AUDIO_FILE)

        diarization_pipeline = initialize_model(MODEL_PATH, HUGGINGFACE_TOKEN)
        asr_pipeline = initialize_asr_pipeline(model_id="lord-reso/whisper-small-inbrowser-proctor")

        perform_diarized_transcription(diarization_pipeline, AUDIO_FILE, EVIDENCE_FILE, asr_pipeline)

        with open(EVIDENCE_FILE, 'r') as file:
            transcription = file.read()
        generate_report(transcription, KEYWORDS_FILE, REPORT_FILE)

        transcripts = read_transcript(EVIDENCE_FILE)
        keywords = read_cheating_keywords(REPORT_FILE)

        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=("Transcript Timeline", "Top 5 Cheating Keywords"),
            specs=[[{"type": "xy"}], [{"type": "domain"}]],
            vertical_spacing=0.3
        )
        create_timeline(fig, transcripts)
        create_pie_chart(fig, keywords)

        fig.update_layout(
            height=1250, 
            showlegend=False,
            title_text="Transcript Timeline Visualization",  
            title_x=0.5, 
            title_font=dict(size=24)
        )
        plot(fig, filename=f'{base_dir}/backend/dashboard/templates/reports/audio_reports/{email}_audioreport.html')
        print("Audio report generated successfully")

        return HttpResponse("Audio report generated successfully")
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return HttpResponseServerError(error_message)
    



