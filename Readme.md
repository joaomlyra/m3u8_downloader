# M3U8 Downloader

Um script em **Python** para baixar vídeos e transmissões a partir de links `.m3u8`.
O script lê o `master.m3u8`, lista as qualidades disponíveis (1080p, 720p, 480p, etc.) e permite ao usuário escolher qual baixar usando **ffmpeg**.

---

## Funcionalidades
- Detecta as qualidades disponíveis em um `master.m3u8`
- Permite escolher manualmente a resolução desejada
- Faz o download direto para `.mp4` sem perda de qualidade
- Usa o `ffmpeg` para juntar os segmentos de forma rápida e eficiente

---

## Melhorias
- Interativo: agora o script solicita via `input`:
- URL do .m3u8
- Nome do arquivo
- Caminho onde o arquivo será salvo
- Permite escolher manualmente a resolução desejada

---

## Correções

- Corrigido o problema de exibir "Download concluído" mesmo quando o ffmpeg falhava
- Adicionada a opção de baixar vários vídeos em sequência sem precisar reiniciar o script 

---

## Requisitos
- Python 3.8+
- [ffmpeg](https://ffmpeg.org/) instalado e disponível no PATH
- Bibliotecas Python:
  - `requests`