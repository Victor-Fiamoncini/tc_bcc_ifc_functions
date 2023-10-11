import os
import subprocess
import wave

AUDIOS_SEM_ROBO_DIR = os.path.join("..", "audios_tc_sem_robo")
AUDIOS_CORTADOS_DIR = os.path.join("..", "audios_sem_robo_cortados")


def get_most_shortest_audio() -> float:
    shortest_duration = float("inf")
    shortest_file = None

    for filename in os.listdir(AUDIOS_SEM_ROBO_DIR):
        if filename.endswith(".wav"):
            filepath = os.path.join(AUDIOS_SEM_ROBO_DIR, filename)

            try:
                with wave.open(filepath, "rb") as audio_file:
                    frames = audio_file.getnframes()
                    frame_rate = audio_file.getframerate()
                    duration = frames / float(frame_rate)

                    if duration < shortest_duration:
                        shortest_duration = duration
                        shortest_file = filename
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    if shortest_file:
        print(
            f"The shortest duration is {shortest_duration} seconds in file: {shortest_file}"
        )

    return shortest_duration


def format_seconds_to_ffmpeg_time_format(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return formatted_time


def cut_audios(to_time: str) -> None:
    for root, _, files in os.walk(AUDIOS_SEM_ROBO_DIR):
        for filename in files:
            filepath = os.path.join(root, filename)
            cutted_audio_path = os.path.join(AUDIOS_CORTADOS_DIR, filename)

            command = f"ffmpeg -i {filepath} -ss 00:00:00 -to {to_time} -c copy {cutted_audio_path}"

            subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )


def get_audio_duration(filepath: str) -> float:
    with wave.open(filepath, "rb") as audio_file:
        framerate = audio_file.getframerate()
        frames = audio_file.getnframes()

        total_seconds = frames / framerate

    return total_seconds


def get_audios_average_duration() -> None:
    durations = []

    for arquivo in os.listdir(AUDIOS_SEM_ROBO_DIR):
        if arquivo.endswith(".wav"):
            filepath = os.path.join(AUDIOS_SEM_ROBO_DIR, arquivo)
            duration = get_audio_duration(filepath)

            durations.append(duration)

    if len(durations):
        duracao_media = sum(durations) / len(durations)

        print(
            f"The average length of the .wav files in the folder is {duracao_media:.2f} seconds or {(duracao_media / 60):.2f} minutes"
        )


get_audios_average_duration()
# cut_audios(format_seconds_to_ffmpeg_time_format(get_most_shortest_audio()))
