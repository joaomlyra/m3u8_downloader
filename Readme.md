# JML Downloader

Um gerenciador de downloads robusto para streams `.m3u8` (HLS), desenvolvido em Python com interface moderna (CustomTkinter). Permite baixar múltiplos vídeos simultaneamente, gerenciar fila e escolher qualidade.

---

## 🔥 Funcionalidades

- **Múltiplos Downloads:** Adicione vários vídeos à fila; eles baixam em paralelo.
- **Detector de Qualidade:** Identifica automaticamente as resoluções disponíveis (1080p, 720p, etc.).
- **Gestão Inteligente:**
  - **Botão Parar/Remover:** Cancele downloads em andamento ou remova os concluídos da lista.
  - **Abrir na Pasta:** Botão direto para localizar o arquivo baixado.
- **Proteção de Dados:** Impede o fechamento acidental se houver downloads ativos.
- **Memória:** O app "lembra" o tamanho e posição da janela e a última pasta usada.
- **Visual:** Interface Dark Mode.

---

## 🏗️ Estrutura do Projeto

O código foi refatorado para alta performance e organização:

- `main.py`: Gerencia a janela principal e orquestra a aplicação.
- `download_engine.py`: O "motor". Controla as threads e o processo do FFmpeg para não travar a tela.
- `ui_components.py`: Contém os elementos visuais (linhas da lista, botões, barras de progresso).

---

## ⚠️ Aviso

Esta ferramenta foi desenvolvida para fins educacionais e de arquivamento pessoal. O usuário é responsável por garantir que possui permissão para baixar o conteúdo das transmissões.

---

Desenvolvido por **(JML)**.