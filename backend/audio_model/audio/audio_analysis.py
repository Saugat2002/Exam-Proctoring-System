from utils.text_utils import generate_report
from scripts.speaker_diarization import initialize_model, diarized_transcription
from scripts.asr_transcribe import initialize_asr_pipeline

def perform_diarized_transcription(finetuned_pipeline, audio_file, output_file, asr_pipeline):
    try:
        diarized_transcription(finetuned_pipeline, audio_file, output_file, asr_pipeline)
    except Exception as e:
        print(f"An error occurred during diarized transcription: {e}")

def main():
    MODEL_PATH = "model/segmentation.ckpt"
    HUGGINGFACE_TOKEN = "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"
    AUDIO_FILE = "webapp/audio/data/audio_files/output_audio.wav"
    EVIDENCE_FILE = "webapp/audio/data/evidence/evidence.txt"
    REPORT_FILE = "webapp/audio/data/evidence/report.txt"
    KEYWORDS_FILE = "webapp/audio/utils/cheating_keywords.txt"

    try:
        finetuned_pipeline = initialize_model(MODEL_PATH, HUGGINGFACE_TOKEN)
        asr_pipeline = initialize_asr_pipeline(model_id="lord-reso/whisper-small-inbrowser-proctor")
    except Exception as e:
        print(f"An error occurred during initialization: {e}")
        return

    perform_diarized_transcription(finetuned_pipeline, AUDIO_FILE, EVIDENCE_FILE, asr_pipeline)

    try:
        with open(EVIDENCE_FILE, 'r') as file:
            transcription = file.read()
        generate_report(transcription, KEYWORDS_FILE, REPORT_FILE)
    except Exception as e:
        print(f"An error occurred during report generation: {e}")

if __name__ == "__main__":
    main()