import requests
import subprocess

def baixar_video():
    # URL do master.m3u8
    master_url = input("\nDigite a URL m3u8: ").strip()

    base_url = master_url.rsplit("/", 1)[0] + "/"

    res = requests.get(master_url)
    lines = res.text.splitlines()

    # Procura resoluções e links relativos
    opcoes = []
    for i, line in enumerate(lines):
        if line.startswith("#EXT-X-STREAM-INF"):
            qualidade = line.split("RESOLUTION=")[-1].split(",")[0]
            link_relativo = lines[i+1]
            opcoes.append((qualidade, link_relativo))

    if not opcoes:
        print("⚠️ Nenhuma qualidade encontrada nesse link.")
        return

    # Mostra opções
    print("\nQualidades disponíveis:")
    for idx, (qualidade, link) in enumerate(opcoes, 1):
        print(f"[{idx}] {qualidade} -> {link}")

    # Escolha do usuário
    escolha = int(input("\nDigite o número da qualidade desejada: ")) - 1
    url_final = base_url + opcoes[escolha][1]

    saida = input("Digite o nome do arquivo de saída (ex: video.mp4): ").strip()

    print(f"\n Baixando de {url_final} para {saida}...\n")
    resultado = subprocess.run([
        "ffmpeg", "-i", url_final, "-c", "copy", "-bsf:a", "aac_adtstoasc", saida
    ])

    # Checa resultado
    if resultado.returncode == 0:
        print("\n✅ Download concluído com sucesso!")
    else:
        print("\n❌ Erro no download. Verifique o link ou o ffmpeg.")

# Loop principal
while True:
    baixar_video()
    repetir = input("\nDeseja baixar outro vídeo? (s/n): ").strip().lower()
    if repetir != "s":
        print("\n👋 Encerrando o programa...")
        break
