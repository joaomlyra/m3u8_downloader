import subprocess
import threading
import os
import time
import re
import datetime

class DownloadTask:
    def __init__(self, url, saida, ui_row, on_finish_callback):
        self.url = url
        self.saida = saida
        self.ui = ui_row
        self.on_finish = on_finish_callback
        self.process = None
        self.cancelado = False
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._worker, daemon=True).start()

    def stop(self):
        self.cancelado = True
        if self.process:
            self.process.kill()

    def _worker(self):
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        cmd = ["ffmpeg", "-i", self.url, "-c", "copy", "-bsf:a", "aac_adtstoasc", "-y", "-progress", "pipe:1", "-nostats", self.saida]

        try:
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, startupinfo=startupinfo)
            
            start_time = time.time()
            last_ui_update = time.time() # Buffer para não travar a UI
            current_size = 0
            total_duration_sec = 0
            
            # Variáveis temporárias para UI
            temp_speed = "0.0 MB/s"
            temp_size = "0.0 MB"
            temp_eta = "--:--:--"
            temp_progress = 0

            while True:
                if self.cancelado:
                    self._cleanup_error("Cancelado")
                    return

                line = self.process.stdout.readline()
                if not line and self.process.poll() is not None: break
                
                if line:
                    line = line.strip()
                    # 1. Pega Duração Total
                    if "Duration:" in line and total_duration_sec == 0:
                        try:
                            dur_str = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})", line)
                            if dur_str:
                                h, m, s = map(float, dur_str.groups())
                                total_duration_sec = h*3600 + m*60 + s
                        except: pass

                    # 2. Pega Progresso
                    key_val = line.split("=")
                    if len(key_val) == 2:
                        k, v = key_val[0].strip(), key_val[1].strip()
                        if k == "total_size":
                            try: current_size = int(v)
                            except: pass
                        if k == "out_time_us":
                            try:
                                cur_time = int(v) / 1000000
                                if total_duration_sec > 0:
                                    temp_progress = cur_time / total_duration_sec
                                    # Calc ETA
                                    elapsed = time.time() - start_time
                                    if temp_progress > 0.01:
                                        eta_s = (elapsed / temp_progress) - elapsed
                                        temp_eta = str(datetime.timedelta(seconds=int(eta_s)))
                                else:
                                    temp_eta = "Live"
                                    # Incremento fake pra live
                                    if temp_progress < 0.95: temp_progress += 0.0001
                            except: pass

                # 3. Atualiza UI apenas a cada 0.5 segundos (Evita o lag/oscilação)
                if time.time() - last_ui_update >= 0.5:
                    elapsed_total = time.time() - start_time
                    if elapsed_total > 0:
                        speed_mb = (current_size / 1024 / 1024) / elapsed_total
                        temp_speed = f"{speed_mb:.2f} MB/s"
                        temp_size = f"{current_size / 1024 / 1024:.2f} MB"
                    
                    # Chama a função visual no arquivo UI
                    self.ui.update_ui(temp_progress, temp_speed, temp_size, temp_eta)
                    last_ui_update = time.time()

            # Fim do Loop
            if self.process.returncode == 0:
                self.ui.update_ui(1.0, "Finalizado", temp_size, "Concluído", "#32D74B")
            else:
                if not self.cancelado:
                    self.ui.update_ui(-1, "Erro", "---", "Falha", "#FF453A")
            
            self.on_finish(self)

        except Exception as e:
            print(f"Erro Thread: {e}")
            self._cleanup_error("Erro Crítico")

    def _cleanup_error(self, msg):
        self.ui.update_ui(0, "---", "---", msg, "#FF453A")
        if self.process: self.process.kill()
        time.sleep(0.5)
        if os.path.exists(self.saida): os.remove(self.saida)
        self.on_finish(self)