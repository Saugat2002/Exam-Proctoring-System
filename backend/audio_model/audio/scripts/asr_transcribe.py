import os
import torch
from transformers import pipeline, AutoModelForSpeechSeq2Seq, AutoTokenizer, WhisperFeatureExtractor
from transformers import pipeline, AutoModelForSpeechSeq2Seq, AutoTokenizer, WhisperFeatureExtractor

def initialize_asr_pipeline(model_id="openai/whisper-small"):
    """
    Initialize the automatic speech recognition (ASR) pipeline.

    Args:
    model_id (str): The identifier for the pre-trained Whisper model. Default is "openai/whisper-small".

    Returns:
    pipeline: The ASR pipeline object.
    """
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    feature_extractor = WhisperFeatureExtractor.from_pretrained(model_id)

    asr_pipeline = pipeline(
        "automatic-speech-recognition",
        model=model,
        chunk_length_s=30,
        tokenizer=tokenizer,
        feature_extractor=feature_extractor, 
        device=device
    )

    return asr_pipeline

def transcribe(asr_pipeline, audio_dir, transcriptions_dir):
    """
    Transcribe audio files using the ASR pipeline and save the transcriptions to a specified directory.

    Args:
    asr_pipeline (pipeline): The ASR pipeline object.
    audio_dir (str): The directory containing the audio files to be transcribed.
    transcriptions_dir (str): The directory where the transcription files will be saved.

    Returns:
    None
    """
    os.makedirs(transcriptions_dir, exist_ok=True)
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]

    for audio_file in audio_files:
        audio_path = os.path.join(audio_dir, audio_file)
        try:
            transcription = asr_pipeline(audio_path)
            transcription_file = os.path.join(transcriptions_dir, f'{os.path.splitext(audio_file)[0]}.txt')
            with open(transcription_file, 'w') as f:
                f.write(transcription['text'])
            print(f'Transcribed {audio_file} and saved to {transcription_file}')
        except Exception as e:
            print(f"Error processing {audio_file}: {e}")
