


from flask import Flask, render_template, request
import assemblyai as aai
import pysrt
aai.settings.api_key = "hid"
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import CompositeVideoClip, TextClip

from openai import OpenAI

client = OpenAI(api_key="sk-hid")

app = Flask(__name__)

def read_text_from_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def translate_text(prompt_text,language):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You will be provided with a block of text , and your task is to convert the text into {language}. Don't mess up the timestamps.",
            },
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
    )
    return response

def handle_subtitles_different(language,file):
    transcribed_text = read_text_from_file(file)
    tags_response = translate_text(transcribed_text, language)

    response_message = tags_response.choices[0].message.content

    with open("static/translated_subtitles.txt", "w") as f:
        f.write(response_message)
    return response_message

def video_to_audio(file_path, audio_file_path):
    video_clip = VideoFileClip(file_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_file_path)


def time_to_seconds(time_obj):
    return (
        time_obj.hours * 3600
        + time_obj.minutes * 60
        + time_obj.seconds
        + time_obj.milliseconds / 1000
    )


def create_subtitle_clips(
    subtitles, videosize, fontsize=24, font="Arial", color="yellow", debug=False
):
    subtitle_clips = []

    for subtitle in subtitles:
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time

        video_width, video_height = videosize

        text_clip = (
            TextClip(
                subtitle.text,
                fontsize=fontsize,
                font=font,
                color=color,
                bg_color="black",
                size=(video_width * 3 / 4, None),
                method="caption",
            )
            .set_start(start_time)
            .set_duration(duration)
        )
        subtitle_x_position = "center"
        subtitle_y_position = video_height * 4 / 5

        text_position = (subtitle_x_position, subtitle_y_position)
        subtitle_clips.append(text_clip.set_position(text_position))

    return subtitle_clips

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'video_to_audio':
            video_file = request.files['file']

            video_path = 'static/uploaded_video.mp4'
            video_file.save(video_path)

            audio_path = 'static/generated_audio.wav'

            video_to_audio(video_path, audio_path)

            return render_template('audio_result.html',audio_path=audio_path)
        elif action == 'video_to_subtitles':

            video_file = request.files['file']
            video_path = 'static/uploaded_video.mp4'
            video_file.save(video_path)
            transcript = aai.Transcriber().transcribe(video_path)
            subtitles = transcript.export_subtitles_srt()
            subtitles_path = 'static/generated_subtitles.srt'
            with open(subtitles_path, 'w') as f:
                f.write(subtitles)

            return render_template('subtitles_result.html', subtitles=subtitles)
        elif action == 'video_with_subtitles':
            video_file = request.files['file']
            video_path = 'static/uploaded_video.mp4'
            video_file.save(video_path)
            transcript = aai.Transcriber().transcribe(video_path)
            subtitles = transcript.export_subtitles_srt()
            subtitles_path = 'static/generated_subtitles.srt'
            with open(subtitles_path, 'w') as f:
                f.write(subtitles)
            
            video = VideoFileClip(video_path)
            subtitles = pysrt.open(subtitles_path)

            
            output_video_file = 'static/subtitled.mp4'

            subtitle_clips = create_subtitle_clips(subtitles, video.size)

            final_video = CompositeVideoClip([video] + subtitle_clips)

            final_video.write_videofile(output_video_file)

            return render_template('video_with_subtitles.html', output_video_path=output_video_file)
        elif action =="subtitles_different":

            language = request.form.get('language')
            video_file = request.files['file']
            video_path = 'static/uploaded_video.mp4'
            video_file.save(video_path)
            transcript = aai.Transcriber().transcribe(video_path)
            subtitles = transcript.export_subtitles_srt()
            subtitles_path = 'static/generated_subtitles.srt'
            with open(subtitles_path, 'w') as f:
                f.write(subtitles)
            final_sub=handle_subtitles_different(language,subtitles_path)
            return render_template('subtitles_lang.html', subtitles=final_sub)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
