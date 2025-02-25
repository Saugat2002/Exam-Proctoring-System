import os
from collections import Counter

def load_cheating_keywords(keywords_file):
    """
    Load cheating keywords from a file.

    Args:
    keywords_file (str): Path to the file containing cheating keywords.

    Returns:
    set: A set of cheating keywords.
    """
    with open(keywords_file, 'r') as file:
        keywords = {line.strip().lower() for line in file}
    return keywords

def detect_cheating_phrases(transcription, keywords_file, threshold=1):
    """
    Detect cheating phrases in a transcription and return their counts.

    Args:
    transcription (str): The transcribed text in which to detect cheating phrases.
    keywords_file (str): Path to the file containing cheating keywords.
    threshold (int): Minimum count for a keyword to be included in the results. Default is 1.

    Returns:
    dict: A dictionary with cheating keywords as keys and their counts as values, filtered by the threshold.
    """
    keywords = load_cheating_keywords(keywords_file)
    transcription = transcription.lower()
    cleaned_transcription = ''.join(char if char.isalnum() or char.isspace() else ' ' for char in transcription)    
    keyword_counts = Counter(word for word in cleaned_transcription.split() if word in keywords)
    filtered_counts = {keyword: count for keyword, count in keyword_counts.items() if count >= threshold}
    
    return filtered_counts

def generate_report(transcription, keywords_file, filename, threshold=1):
    """
    Generate a report from the detected cheating phrases.

    Args:
    transcription (str): The transcribed text.
    keywords_file (str): Path to the file containing cheating keywords.
    filename (str): The name of the output report file.
    threshold (int): Minimum count for a keyword to be included in the report.
    """
    detected_cheating_phrases = detect_cheating_phrases(transcription, keywords_file, threshold)
    report_content = f"Report on {filename}\nCheating Keywords detected:\n"
    
    for keyword, count in detected_cheating_phrases.items():
        report_content += f"{keyword.capitalize()}: {count}\n"
    
    with open(filename, 'w') as report_file: 
        report_file.write(report_content)
    
    print(f"Report generated successfully and saved to {filename}")