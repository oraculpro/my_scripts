import os
import subprocess
import tempfile
from pydub import AudioSegment
import speech_recognition as sr


def extract_audio(video_path):
    base = os.path.splitext(video_path)[0]
    audio_file = f"{base}.wav"

    # Извлечь аудио с помощью ffmpeg
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '16000',
        '-ac', '1',
        audio_file,
        '-y'
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"🔊 Аудио извлечено: {audio_file}")
    return audio_file


def transcribe_audio_chunks(audio_path, chunk_length_ms=50000):  # 50 секунд
    sound = AudioSegment.from_wav(audio_path)
    chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]

    recognizer = sr.Recognizer()
    full_text = ""

    for i, chunk in enumerate(chunks):
        chunk_filename = os.path.join(tempfile.gettempdir(), f"chunk_{i}.wav")
        chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            audio = recognizer.record(source)

        try:
            print(f"🧠 Распознаём часть {i+1}/{len(chunks)}...")
            text = recognizer.recognize_google(audio, language="ru-RU")
            full_text += f"[Часть {i+1}]\n{text}\n\n"
        except sr.UnknownValueError:
            print(f"❌ Не удалось распознать часть {i+1}")
        except sr.RequestError as e:
            print(f"⚠️ Ошибка сервиса распознавания: {e}")
            break  # Если сервис недоступен — дальше не пытаться

        os.remove(chunk_filename)

    return full_text


def save_text_to_file(text, video_path):
    base = os.path.splitext(video_path)[0]
    txt_file = f"{base}.txt"
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"📄 Текст сохранён в: {txt_file}")


def main(video_path):
    if not os.path.isfile(video_path):
        print("❌ Файл не найден.")
        return

    wav_file = extract_audio(video_path)
    full_text = transcribe_audio_chunks(wav_file)

    if full_text.strip():
        save_text_to_file(full_text, video_path)
    else:
        print("❌ Ни одна часть не была распознана.")

    # Удалить временный WAV файл
    if os.path.exists(wav_file):
        os.remove(wav_file)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python extract_text_from_audio_improved.py <путь_к_видео>.mp4")
    else:
        main(sys.argv[1])

# pip install pydub SpeechRecognition ffmpeg-python
