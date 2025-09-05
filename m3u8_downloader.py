import subprocess

# Pergunta ao usuário
url = input("Digite a URL .m3u8: ").strip()
saida = input("Digite o caminho e nome do arquivo (ex: video.mp4): ").strip()

# Executa o ffmpeg
comando = [
    "ffmpeg",
    "-i", url,                # entrada (input)
    "-c", "copy",             # copia os streams sem re-encodar (rápido e sem perda)
    "-bsf:a", "aac_adtstoasc",# filtro pra corrigir áudio AAC em alguns players
    saida                     # arquivo de saída
]

print(f"\n Baixando vídeo de {url} para {saida} ...\n")
subprocess.run(comando)
print("\n Download concluído!")
