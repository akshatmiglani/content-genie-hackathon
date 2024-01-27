# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, render_template, request

# app = Flask(__name__)
# ALLOWED_EXTENSIONS=['mp4']

# @app.route('/')
# def index():
#     return render_template('index.html')

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/upload',methods=['POST'])
# def upload():
#     if 'video' not in request.files:
#         return "No video file found"
#     video=request.files['video']
#     if video.filename=="":
#         return "No video selected"
#     if video and allowed_file(video.filename):
#         video.save('static/'+video.filename)
#         return render_template('preview.html',video_name=video.filename)
#     return "INVALID"




# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request
import assemblyai as aai
import pysrt
aai.settings.api_key = "c9237cb068cb471689f9a4a98f5f1b34"
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import CompositeVideoClip, TextClip



app = Flask(__name__)

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

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
