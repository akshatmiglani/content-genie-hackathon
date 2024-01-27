from openai import OpenAI
import os
client = OpenAI(api_key="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")

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_tags_chat(prompt_text):
    response =client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You will be provided with a block of text , and your task is to convert the text into Spanish and it should be according to the timestamps. In the ouput file, add '--' for specific pauses and when this is read it should be of 53 seconds."},
            {"role": "user", "content": """ 1
00:00:00,970 --> 00:00:03,360
Samaya. Come in. Yes, come in. Thank you.

2
00:00:05,090 --> 00:00:08,906
Good morning, sir. Good morning. Good morning, ma'am. Take a seat.

3
00:00:08,938 --> 00:00:10,240
A chad. Thank you, sir.

4
00:00:12,050 --> 00:00:15,358
Akshad Jain. Yes, sir. Give you

5
00:00:15,364 --> 00:00:18,606
a brief description about yourself. So, my name

6
00:00:18,628 --> 00:00:22,218
is Aksha Jain. I am 23 years old. I was born in Jaipur,

7
00:00:22,234 --> 00:00:25,446
Rajasthan, from where I've done my high schooling. And I done my

8
00:00:25,468 --> 00:00:28,566
bachelor's in design from IIT Guwahati. And so

9
00:00:28,588 --> 00:00:32,454
my interests include fitness, swimming, football. And so this is

10
00:00:32,492 --> 00:00:36,070
going to be my second attempt at UPSC and my first interview.

11
00:00:36,810 --> 00:00:39,670
We're going through your detailed application form,

12
00:00:39,740 --> 00:00:43,254
sir. And we have come to know that both your parents are already

13
00:00:43,292 --> 00:00:46,854
civil servants. Yes, sir. They are in the police service or,

14
00:00:47,052 --> 00:00:50,366
sir, my father is in the police service. My mother is in the revenue service.

15
00:00:50,468 --> 00:00:51,630
She is in the rain.

"""}
        ],
        temperature=0.5,
        max_tokens=1000,
        top_p=1
    )
    return response


transcribed_text = read_text_from_file("static\generated_subtitles.srt")
tags_response = generate_tags_chat(transcribed_text)

response_message = tags_response.choices[0].message.content

with open("tags.txt", "w") as f:
    f.write(response_message)