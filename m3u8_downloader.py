import subprocess

url = "SEU LINK .M3U8"
saida = "C:\\downloads\\video.mp4"

subprocess.run([
    "ffmpeg",
    "-i", url,
    "-c", "copy",
    "-bsf:a", "aac_adtstoasc",
    saida
])
