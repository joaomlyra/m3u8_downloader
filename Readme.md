# M3U8 Downloader

Um aplicativo desktop desenvolvido em **Python** com interface gráfica nativa (**Tkinter**) para baixar vídeos e transmissões a partir de links `.m3u8` de forma simples, sem necessidade de comandos no terminal.

O programa lê a lista mestra, identifica as qualidades disponíveis e utiliza o **FFmpeg** para processar o download com máxima eficiência.

---

## 🚀 Funcionalidades

- **Interface Gráfica (GUI):** Janela amigável com botões e menus, eliminando o uso do terminal.
- **Detector de Qualidade:** Analisa o link e lista automaticamente as resoluções disponíveis (1080p, 720p, 480p, etc.).
- **Salvar Como:** Utiliza a janela nativa do sistema para você escolher exatamente onde salvar o arquivo e qual nome dar.
- **Log Integrado:** Visualização em tempo real do status da conexão e do processo do FFmpeg.
- **Download em Background:** O processo roda em uma *thread* separada, garantindo que a janela não trave durante o download.

---

## 📋 Pré-requisitos

Para executar este projeto, você precisa de:

1.  **Python 3.8+** instalado.
2.  **FFmpeg** instalado e configurado nas variáveis de ambiente (PATH) do sistema.
3.  Biblioteca `requests` instalada (`pip install requests`).

---

## 🛠️ Como Usar

1.  Execute o script:
    ```bash
    python nome_do_arquivo.py
    ```
2.  **Cole a URL** do arquivo `.m3u8` no campo indicado.
3.  Clique no botão **"🔍 Buscar Qualidades"**.
4.  Selecione a resolução desejada na lista que aparecerá.
5.  Clique em **"⬇️ Baixar Vídeo"**.
6.  Uma janela abrirá perguntando **onde você deseja salvar** o arquivo `.mp4`.
7.  Acompanhe o progresso na barra e no log de texto.

---

## ⚙️ Tecnologias

- **Python 3**: Linguagem principal.
- **Tkinter**: Biblioteca padrão para a interface gráfica (GUI).
- **Requests**: Para requisições HTTP e leitura das playlists.
- **Subprocess**: Para execução e controle do FFmpeg.
- **Threading**: Para gerenciamento de processos simultâneos.

---

## ⚠️ Aviso

Esta ferramenta foi desenvolvida para fins educacionais e de arquivamento pessoal. O usuário é responsável por garantir que possui permissão para baixar o conteúdo das transmissões.

---

Desenvolvido por **(JML)**.