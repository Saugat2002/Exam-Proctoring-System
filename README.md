## Running the backend

cd backend

conda env create -f env.yaml
conda activate proctoring_env


#### Install dependencies
pip install -r requirements.txt

#### Run migrations
python manage.py migrate

#### Start Django server
python manage.py runserver


=================================================================================================

# Inbrowser-Proctoring-2

## Introduction
**Inbrowser Proctoring** is an effective online proctoring application designed to ensure the integrity of examinations by monitoring test-takers in real-time. By leveraging advanced technologies such as video, audio, and screen recording, combined with sophisticated AI algorithms, this system effectively supervises exams and helps prevent cheating. The application analyzes audio and visual data to identify suspicious behaviors, allowing for the immediate detection of anomalies that may indicate dishonest practices. This proactive approach not only helps uphold the standards of the examination process but also provides peace of mind for educators and institutions.

### Key Features
1. **Browser Monitoring**
   - Full-screen Monitoring
   - Tab Activity Detection
   - Generate Real-time Warnings

2. **Audio Cheating Detection**
   - Speaker Diarization
   - Audio Transcription and Analysis

3. **Video Cheating Detection**
   - Object Detection
   - Head Pose Tracking
   - Open Mouth Tracking

4. **Admin Dashboard**
   - Creation and management of online exams
   - Audio and Video Analysis Report


## Goals
The primary objective of this project is to develop a robust proctoring system designed to supervise exams and assessments in an online environment. Our specific goals are as follows:
* To monitor the exam environment in real-time using webcam video and generate warnings
* To track user activities in the browser for suspicious behavior
* To process and analyze audio for transcript analysis and speaker diarization
* To generate report containing audio and video analysis results


## Contributors
The key contributors for this project and their specific roles are as follows:

| Name                   | Project Contribution              | Description                         |
|------------------------|-----------------------------------|-------------------------------------|
| Aayush Man Shrestha    | ASR Based Cheating Detection      | Implemented the automated speech recognition module for detecting cheating. |
| Aditya Bajracharya     | Speaker Diarization               | Implemented speaker diarization to differentiate between multiple speakers during assessments. |
| Anmol Kumar Gupta      | Object Detection                  | Implemented the object detection features to identify prohibited items in the exam environment. |
| Atul Shreewastav      | Facial Landmark Detection         | Implemented algorithms for detecting facial landmarks to monitor test-taker behavior. |
| Khem Raj Shrestha      | Browser Lockdown                  | Built the browser lockdown functionality to prevent suspicious browser activities during exams. |

Furthermore, the contributors were not limited to their particular fields; they also supported each other throughout the project, fostering collaboration and enhancing the overall quality of the work.


## Project Architecture


# Status
## Known Issue
## High Level Next Steps


# Usage
## Installation
To begin this project, use the included `Makefile`

#### Creating Virtual Environment

This package is built using `python-3.8`. 
We recommend creating a virtual environment and using a matching version to ensure compatibility.

#### pre-commit

`pre-commit` will automatically format and lint your code. You can install using this by using
`make use-pre-commit`. It will take effect on your next `git commit`

#### pip-tools

The method of managing dependencies in this package is using `pip-tools`. To begin, run `make use-pip-tools` to install. 

Then when adding a new package requirement, update the `requirements.in` file with 
the package name. You can include a specific version if desired but it is not necessary. 

To install and use the new dependency you can run `make deps-install` or equivalently `make`

If you have other packages installed in the environment that are no longer needed, you can you `make deps-sync` to ensure that your current development environment matches the `requirements` files. 

## Usage Instructions


# Data Source
The project uses 2 datasets:
* **Inbrowser Proctor Dataset:** A custom dataset of whispers and low-intensity recitations of cheating keywords and phrases, created for fine-tuning Whisper model.
* **AMI Speech Corpus:** An open-source dataset of meeting recordings, used for fine-tuning Pyannote for speaker diarization. The audio intesity has been reduced my 8 dB to simulate low-intensity conditions.

A summary and comparison of datasets is present below:

| Description                      | Inbrowser Proctor Dataset | AMI Speech Corpus (mini) |
|----------------------------------|--------------------------|--------------------------|
| Audio Format                     | wav (256 kbps)          | wav (256 kbps)          |
| Total Duration                   | ~4 hours                 | ~10.5 hours             |
| Number of Audio Clips            | 505                      | 34                       |
| Average Clip Duration            | 28 sec                  | 25 min                  |
| Number of Speakers               | 5                        | 136                      |
| Language                         | English (Nepali accent)  | English                  |
| Split                            | train:validation split (85:15) | train:dev:test split (28:3:3) |

## Code Structure
- **frontend/**: Consists of all the code from conducting exams to recording video and generating realtime warnings.

In the **backend/**, the project is organized as follows:
- **mcq/:** Fetches MCQ questions from database for exam.
- **audio_model/**
  - **scripts/speaker_diarization.py**: Implements speaker diarization using Pyannote to identify and segment different speakers in the audio recordings.
  - **scripts/asr_transcribe.py**: Handles automatic speech recognition (ASR) using Whisper to generate transcripts from audio.
  - **views.py**: Manages the integration of audio models with the Django backend.

- **video_model/**
  - **views.py**: Manages video processing tasks (object detection and head pose tracking) in conjunction with the Django backend.

- **dashboard/** 
  - **templates/**: Consists of html templates for final audio and video reports.
  - **views.py**: Displays the exam and examinee info along with final cheating analysis reports.
## Artifacts Location
- **Audio Reports**: Speaker diarization result and transcripts are stored in the [report/](./backend/audio_model/audio/data/evidence/) directory.
- **Recordings**: Webcam feed recording and extracted audio are saved in the [proctoring_videos/](./backend/media/proctoring_videos/) and [audio_files/](./backend/audio_model/audio/data/audio_files/) directory respectively.
- **Models**: The pretrained and finetuned models for audio and video processing are stored in [model/](./backend/audio_model/audio/model/) directory.
- **Final HTML Report**: The final .html report rendered in the dashboard is present in the [templates/](./backend/dashboard/templates/) directory.

# Results
## Metrics Used
## Evaluation Results