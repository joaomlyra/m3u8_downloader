# M3U8 Downloader

Um script em **Python** para baixar vídeos e transmissões a partir de links `.m3u8`.

---

## Funcionalidades
- Faz o download direto para `.mp4` sem perda de qualidade
- Usa o `ffmpeg` para juntar os segmentos de forma rápida e eficiente

---

## Melhorias
- **Interativo:**agora o script solicita via `input`:
- URL do .m3u8
- Nome do arquivo
- Caminho onde o arquivo será salvo

---

## Requisitos
- Python 3.8+
- [ffmpeg](https://ffmpeg.org/) instalado e disponível no PATH
- Bibliotecas Python:
  - `requests`