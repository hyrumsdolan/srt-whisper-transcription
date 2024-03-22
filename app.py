from datetime import timedelta
import os
import whisper
import argparse

def transcribe_audio(path, output_dir):
    model = whisper.load_model("base")  # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    srt_filename = os.path.splitext(os.path.basename(path))[0] + ".srt"
    srt_filepath = os.path.join(output_dir, srt_filename)

    with open(srt_filepath, 'w', encoding='utf-8') as srt_file:
        for segment in segments:
            start_time = str(timedelta(seconds=int(segment['start']))) + ',000'
            end_time = str(timedelta(seconds=int(segment['end']))) + ',000'
            text = segment['text']
            segment_id = segment['id'] + 1
            segment_text = f"{segment_id}\n{start_time} --> {end_time}\n{text.strip()}\n\n"
            srt_file.write(segment_text)

    print(f"SRT file generated: {srt_filepath}")
    return srt_filepath

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transcribe audio to SRT using Whisper')
    parser.add_argument('audio_file', type=str, help='Path to the audio file')
    parser.add_argument('--output_dir', type=str, default='SrtFiles', help='Output directory for the SRT file')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    transcribe_audio(args.audio_file, args.output_dir)