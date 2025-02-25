import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot

def read_transcript(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    pattern = r'Speaker (?P<speaker>SPEAKER_\d+):\s+Start: (?P<start>\d+\.\d+)s, End: (?P<end>\d+\.\d+)s\s+Transcript: (?P<transcript>.+?)(?:\n\n|\Z)'
    matches = re.finditer(pattern, data, re.DOTALL)

    transcripts = []
    for match in matches:
        transcripts.append({
            'speaker': match.group('speaker'),
            'start': float(match.group('start')),
            'end': float(match.group('end')),
            'transcript': match.group('transcript').strip()
        })

    return transcripts

def create_timeline(fig, transcripts):
    colors = {
        'SPEAKER_01': 'skyblue',
        'SPEAKER_02': 'lightgreen',
        'SPEAKER_03': 'orange',
        'SPEAKER_04': 'plum',
        'SPEAKER_05': 'gold',
        'SPEAKER_06': 'lightgrey'
    }
    default_color = 'lightcoral'

    for transcript in transcripts:
        color = colors.get(transcript['speaker'], default_color)
        fig.add_trace(go.Bar(
            x=[transcript['end'] - transcript['start']],
            y=[transcript['speaker']],
            text=transcript['transcript'],
            hoverinfo='text',
            textposition='none',
            orientation='h',
            marker=dict(color=color),
            base=transcript['start']
        ), row=1, col=1)

    fig.update_xaxes(
        title_text='Time (s)',
        rangeslider=dict(visible=True),
        type='linear',
        row=1, col=1
    )
    fig.update_yaxes(
        title_text='Speaker',
        tickmode='array',
        tickvals=[t['speaker'] for t in transcripts],
        ticktext=[t['speaker'] for t in transcripts],
        row=1, col=1
    )

    fig.update_layout(
        title='Transcript and Cheating Keywords Analysis',
        barmode='stack',
        showlegend=False,
        autosize=True,
        height=800,
        margin=dict(l=50, r=50, b=50, t=50, pad=4)
    )

def read_cheating_keywords(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    pattern = r'(\w+): (\d+)'
    matches = re.findall(pattern, data)

    keywords = {}
    for match in matches:
        keyword, count = match
        keywords[keyword] = int(count)

    return keywords


def create_pie_chart(fig, keywords):
    sorted_keywords = sorted(keywords.items(), key=lambda item: item[1], reverse=True)[:5]
    labels = [item[0] for item in sorted_keywords]
    values = [item[1] for item in sorted_keywords]

    fig.add_trace(
        go.Pie(
            labels=labels, 
            values=values, 
            hole=0.3, 
            hoverinfo='label+value',
            textinfo='label',
            textposition='inside',
            insidetextfont=dict(color='white'),
            outsidetextfont=dict(color='white')
        ), 
        row=2, 
        col=1
    )
    fig.update_layout(
        annotations=[
            dict(
                text='Top 5 Cheating Keywords',
                x=0.5,
                y=0.35,
                font=dict(size=20),
                showarrow=False,
                xref="paper",
                yref="paper"
            )
        ],
        height=800,
        margin=dict(t=100)
    )

def main():
    transcript_file_path = r'C:\Users\atuls\OneDrive\Desktop\final\backend\audio_model\audio\data\evidence\evidence.txt'
    report_file_path = r'C:\Users\atuls\OneDrive\Desktop\final\backend\audio_model\audio\data\report\report.txt'
    transcripts = read_transcript(transcript_file_path)
    keywords = read_cheating_keywords(report_file_path)

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
    plot(fig, filename='audio_report.html')

if __name__ == '__main__':
    main()
