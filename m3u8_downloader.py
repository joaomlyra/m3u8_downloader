import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import subprocess
import threading
import sys
import re
import os

class BaixadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Baixador de Lives (m3u8)")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        # Variáveis
        self.url_var = tk.StringVar()
        self.opcoes_qualidade = []
        self.link_final = ""

        # --- Layout ---
        
        # 1. Entrada de URL
        lbl_url = ttk.Label(root, text="Cole a URL do .m3u8:")
        lbl_url.pack(pady=(10, 0))
        
        entry_url = ttk.Entry(root, textvariable=self.url_var, width=60)
        entry_url.pack(pady=5)
        
        btn_buscar = ttk.Button(root, text="🔍 Buscar Qualidades", command=self.buscar_qualidades)
        btn_buscar.pack(pady=5)

        # 2. Seleção de Qualidade
        lbl_qualidade = ttk.Label(root, text="Selecione a Qualidade:")
        lbl_qualidade.pack(pady=(15, 0))
        
        self.combo_qualidade = ttk.Combobox(root, state="readonly", width=30)
        self.combo_qualidade.pack(pady=5)

        # 3. Botão de Download
        self.btn_baixar = ttk.Button(root, text="⬇️ Baixar Vídeo", state="disabled", command=self.iniciar_download_thread)
        self.btn_baixar.pack(pady=15)

        # 4. Barra de Progresso
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)
        
        self.lbl_status = ttk.Label(root, text="Aguardando...")
        self.lbl_status.pack()

        # 5. Log de Texto (Para ver o que está acontecendo)
        self.log_text = tk.Text(root, height=8, width=55, state="disabled", font=("Consolas", 8))
        self.log_text.pack(pady=10)

    def log(self, mensagem):
        """Escreve no log da interface"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, mensagem + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def buscar_qualidades(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Digite uma URL primeiro!")
            return

        self.log(f"Buscando qualidades em: {url}...")
        
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            lines = res.text.splitlines()
            base_url = url.rsplit("/", 1)[0] + "/"
            
            self.opcoes_qualidade = []
            
            # Lógica de parsing (igual ao script anterior)
            temp_opcoes = []
            for i, line in enumerate(lines):
                if line.startswith("#EXT-X-STREAM-INF"):
                    res_match = re.search(r'RESOLUTION=(\d+x\d+)', line)
                    qualidade = res_match.group(1) if res_match else "Unknown"
                    link_relativo = lines[i+1]
                    
                    link_completo = link_relativo if link_relativo.startswith("http") else base_url + link_relativo
                    temp_opcoes.append(f"{qualidade}")
                    self.opcoes_qualidade.append(link_completo)

            if not temp_opcoes:
                # Caso seja link direto
                self.opcoes_qualidade.append(url)
                temp_opcoes.append("Qualidade Única/Direta")

            self.combo_qualidade['values'] = temp_opcoes
            self.combo_qualidade.current(0)
            self.btn_baixar.config(state="normal")
            self.log("✅ Qualidades encontradas!")

        except Exception as e:
            self.log(f"❌ Erro ao buscar: {e}")
            messagebox.showerror("Erro", f"Falha ao conectar:\n{e}")

    def iniciar_download_thread(self):
        """Inicia o download em uma thread separada para não travar a tela"""
        idx = self.combo_qualidade.current()
        if idx == -1: return

        url_final = self.opcoes_qualidade[idx]
        
        # Janela para salvar arquivo
        caminho_salvar = filedialog.asksaveasfilename(defaultextension=".mp4", 
                                                      filetypes=[("MP4 files", "*.mp4")],
                                                      title="Salvar vídeo como")
        if not caminho_salvar: return

        self.btn_baixar.config(state="disabled")
        self.progress['value'] = 0
        
        # Cria e inicia a thread
        t = threading.Thread(target=self.rodar_ffmpeg, args=(url_final, caminho_salvar))
        t.start()

    def rodar_ffmpeg(self, url, saida):
        self.log(f"🚀 Iniciando download para: {os.path.basename(saida)}")
        
        # Comando para rodar ffmpeg
        # Importante: startupinfo esconde a janela preta do ffmpeg que pisca no fundo
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        cmd = [
            "ffmpeg", "-i", url, "-c", "copy", "-bsf:a", "aac_adtstoasc", 
            "-y", "-progress", "pipe:1", "-nostats", saida
        ]

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                       universal_newlines=True, startupinfo=startupinfo)
            
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                
                if line:
                    # Atualiza barra de progresso (visual fake ou baseado em tempo se quiser melhorar depois)
                    # Como m3u8 não tem tamanho fixo no header as vezes, vamos fazer a barra andar
                    if "frame=" in line or "size=" in line:
                         self.progress.step(0.1) 
                    
                    # Se quiser logar detalhes técnicos, descomente abaixo:
                    # if "speed" in line: self.log(line.strip())

            if process.returncode == 0:
                self.log("✅ Download Concluído com Sucesso!")
                self.lbl_status.config(text="Sucesso!")
                self.progress['value'] = 100
                messagebox.showinfo("Sucesso", "Download finalizado!")
            else:
                self.log("❌ Erro no FFmpeg.")
                
        except FileNotFoundError:
            self.log("❌ ERRO: ffmpeg.exe não encontrado!")
            messagebox.showerror("Erro", "O arquivo ffmpeg.exe não está na pasta ou no sistema.")
        except Exception as e:
            self.log(f"❌ Erro: {str(e)}")
        finally:
            self.btn_baixar.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = BaixadorApp(root)
    root.mainloop()