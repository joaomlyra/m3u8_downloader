import requests
import subprocess
import os

# URL do master.m3u8
master_url = input("Digite a URL m3u8: ").strip()

# Extrai a base (tudo até a pasta 'hls/')
base_url = master_url.rsplit("/", 1)[0] + "/"

# Baixa o conteúdo
res = requests.get(master_url)
lines = res.text.splitlines()

# Procura resoluções e links relativos
opcoes = []
for i, line in enumerate(lines):
    if line.startswith("#EXT-X-STREAM-INF"):
        qualidade = line.split("RESOLUTION=")[-1].split(",")[0]
        link_relativo = lines[i+1]
        opcoes.append((qualidade, link_relativo))

# Mostra as opções
print("\nQualidades disponíveis:")
for idx, (qualidade, link) in enumerate(opcoes, 1):
    print(f"[{idx}] {qualidade} -> {link}")

# Escolha do usuário
escolha = int(input("\nDigite o número da qualidade desejada: ")) - 1
url_final = base_url + opcoes[escolha][1]

saida = input("Digite o nome do arquivo de saída (ex: video.mp4): ").strip()

# Baixa com ffmpeg
print(f"\n Baixando de {url_final} para {saida} ...\n")
subprocess.run([
    "ffmpeg", "-i", url_final, "-c", "copy", "-bsf:a", "aac_adtstoasc", saida
])
print("\n Download concluído!")
