from gtts import gTTS
import os

# Text you want to convert to speech
text_to_speak = """ Samaya. Adelante. S�, adelante. Gracias.
Buenos d�as, se�or. Buenos d�as. Buenos d�as, se�ora. Tomen asiento.
Un chad. Gracias, se�or.
Akshad Jain. S�, se�or. Te doy
una breve descripci�n sobre ti mismo. As� que, mi nombre es
Aksha Jain. Tengo 23 a�os. Nac� en Jaipur,
Rajast�n, donde hice mi educaci�n secundaria. Y hice mi
licenciatura en dise�o en el IIT Guwahati. Y as�
mis intereses incluyen fitness, nataci�n, f�tbol. Y este ser�
mi segundo intento en el UPSC y mi primera entrevista.
Estamos revisando tu formulario de solicitud detallado,
se�or. Y nos hemos enterado de que ambos de tus padres ya son
funcionarios p�blicos. S�, se�or. Ellos est�n en el servicio de polic�a o,
se�or, mi padre est� en el servicio de polic�a. Mi madre est� en el servicio de ingresos.
Ella est� en la lluvia."""

# Specify the language (in this case, 'es' for Spanish)
language = 'es'

# Create a gTTS object
tts = gTTS(text=text_to_speak, lang=language, slow=False)

# Save the speech as an audio file (you can also play it directly)
tts.save("output.mp3")

# Play the generated audio file (optional)
os.system("start output.mp3")
