import torch
from pyannote.audio import Pipeline, Model
from pyannote.audio.pipelines import SpeakerDiarization
from pyannote.audio import Audio
import soundfile as sf

def initialize_model(model_path, huggingface_token):
    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    checkpoint = torch.load(model_path, map_location=torch.device(device))
    
    if 'state_dict' in checkpoint:
        state_dict = checkpoint['state_dict']
    else:
        raise ValueError("Expected key 'state_dict' not found in checkpoint.")
    
    model = Model.from_pretrained("pyannote/segmentation", use_auth_token=huggingface_token)
    model.load_state_dict(state_dict, strict=False)
    
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=huggingface_token)

    finetuned_pipeline = SpeakerDiarization(
        segmentation=model,
        embedding=pipeline.embedding,
        embedding_exclude_overlap=pipeline.embedding_exclude_overlap,
        clustering=pipeline.klustering,
    )

    finetuned_pipeline.instantiate({
        "segmentation": {
            "threshold": 0.5,
            "min_duration_off": 0,
        },
        "clustering": {
            "method": "centroid",
            "min_cluster_size": 15,
            "threshold": 0.7,
        },
    })

    return finetuned_pipeline

def diarized_transcription(pipeline, audio_file_path, output_path, asr_pipeline): 
    io = Audio(mono='downmix', sample_rate=16000)  # Ensure mono audio with downmix
    waveform, sample_rate = io(audio_file_path)

    diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})

    with open(output_path, 'w') as file:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            start_sample = int(turn.start * sample_rate)
            end_sample = int(turn.end * sample_rate)
            segment_waveform = waveform[:, start_sample:end_sample]
            
            # Convert the segment to mono if necessary
            if segment_waveform.ndim > 1:
                segment_waveform = segment_waveform.mean(axis=0) 
            
            # Transcribe the mono waveform
            transcription = asr_pipeline(segment_waveform.numpy())
            transcript_text = transcription['text']
            
            # Write the result to the output file
            file.write(f"Speaker {speaker}:\n")
            file.write(f"  Start: {turn.start:.2f}s, End: {turn.end:.2f}s\n")
            file.write(f"  Transcript: {transcript_text}\n")
            file.write("\n")