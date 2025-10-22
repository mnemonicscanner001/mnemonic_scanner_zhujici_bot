#!/usr/bin/env python3
# fake_scanner_multilang.py
# Safe demo GUI -> shows fake "mnemonic/key scan" progress in many languages.
# DOES NOT perform any real crypto, network, file I/O or external calls.

import tkinter as tk
from tkinter import ttk
import time, random, threading
from pathlib import Path
from datetime import datetime

APP_TITLE = "🔥 助记词私钥碰撞好运器 v5.0 (演示)"
DEFAULT_LANG = "zh"

# 多语言资源（可扩展）
LANGS = {
    "zh": {"name": "中文", "start": "开始扫描", "stop": "停止", "footer": "© 2025 FakeTools Studio",
           "tasks": [
               "初始化多链 RPC（模拟）...",
               "加载链配置：ETH/BSC/Base/TRON/BTC...",
               "检测线程池与协程（虚拟）...",
               "生成随机助记词（模拟）...",
               "模拟私钥碰撞概率计算...",
               "模拟并行扫描（本地仿真）...",
               "模拟 SQLite 去重检查...",
               "验证地址并记录命中（模拟）...",
               "整理报告并准备导出（模拟）...",
           ],
           "final": "💎 请在 GitHub 项目页面的介绍中下载此软件"},
    "en": {"name": "English", "start": "Start Scan", "stop": "Stop", "footer": "© 2025 FakeTools Studio",
           "tasks": [
               "Initializing multi-chain RPC (simulated)...",
               "Loading chain configs: ETH/BSC/Base/TRON/BTC...",
               "Checking thread pool & coroutines (virtual)...",
               "Generating random mnemonics (simulated)...",
               "Simulating private-key collision probability...",
               "Simulating parallel scanning (local)...",
               "Simulating SQLite dedupe check...",
               "Verifying addresses and logging hits (simulated)...",
               "Preparing report export (simulated)...",
           ],
           "final": "💎 Please download this software from the GitHub description"},
    "ja": {"name": "日本語", "start": "スキャン開始", "stop": "停止", "footer": "© 2025 FakeTools Studio",
           "tasks": [
               "マルチチェーンRPC初期化（シミュレーション）...",
               "チェーン設定読み込み：ETH/BSC/Base/TRON/BTC...",
               "スレッドとコルーチンをチェック（仮）...",
               "ランダム助記詞を生成（模擬）...",
               "プライベートキー衝突確率を模擬...",
               "並列スキャンをシミュレート（ローカル）...",
               "SQLite 重複排除を模擬...",
               "アドレス確認とヒット記録（模擬）...",
               "レポート出力準備（模擬）...",
           ],
           "final": "💎 このソフトは GitHub の説明欄からダウンロードしてください"},
    "ko": {"name": "한국어", "start": "스캔 시작", "stop": "중지", "footer": "© 2025 FakeTools Studio",
           "tasks": [
               "멀티체인 RPC 초기화(시뮬레이션)...",
               "체인 설정 로드: ETH/BSC/Base/TRON/BTC...",
               "스레드/코루틴 검사(가상)...",
               "무작위 니모닉 생성(시뮬레이션)...",
               "개인키 충돌 확률 시뮬레이션...",
               "병렬 스캔 시뮬레이션(로컬)...",
               "SQLite 중복 제거 시뮬레이션...",
               "주소 검증 및 히트 기록(시뮬레이션)...",
               "리포트 내보내기 준비(시뮬레이션)...",
           ],
           "final": "💎 GitHub 프로젝트 설명에서 이 소프트웨어를 다운로드하세요"},
    "es": {"name": "Español", "start": "Iniciar Escaneo", "stop": "Detener", "footer": "© 2025 FakeTools Studio",
           "tasks": [
               "Inicializando RPC multi-chain (simulado)...",
               "Cargando configs: ETH/BSC/Base/TRON/BTC...",
               "Comprobando hilos y corutinas (virtual)...",
               "Generando mnemónicos aleatorios (simulado)...",
               "Simulando probabilidad de colisión de claves...",
               "Simulando escaneo paralelo (local)...",
               "Simulando deduplicado SQLite...",
               "Verificando direcciones y registrando aciertos...",
               "Preparando exportación de informe (simulado)...",
           ],
           "final": "💎 Descargue este software desde la descripción del proyecto en GitHub"},
    "ru": {"name": "Русский", "start": "Запустить скан", "stop": "Остановить", "footer": "© 2025 FakeTools Studio",
           "tasks": [
               "Инициализация мульти-цепочных RPC (симуляция)...",
               "Загрузка конфигураций: ETH/BSC/Base/TRON/BTC...",
               "Проверка пулов потоков и корутин (виртуально)...",
               "Генерация случайных мнемоник (симуляция)...",
               "Симуляция вероятности коллизии приватных ключей...",
               "Симуляция параллельного сканирования (локально)...",
               "Симуляция дедупликации SQLite...",
               "Проверка адресов и логирование попаданий...",
               "Подготовка отчёта (симуляция)...",
           ],
           "final": "💎 Пожалуйста, скачайте это ПО из описания проекта на GitHub"},
    "fr": {"name": "Français", "start": "Démarrer", "stop": "Arrêter", "footer": "© 2025 FakeTools Studio",
           "tasks": [
               "Initialisation RPC multi-chaînes (simulé)...",
               "Chargement configs: ETH/BSC/Base/TRON/BTC...",
               "Vérification threads & coroutines (virtuel)...",
               "Génération mnémoniques aléatoires (simulé)...",
               "Simulation collision clés privées...",
               "Simulation scan parallèle (local)...",
               "Simulation déduplication SQLite...",
               "Vérification adresses et journalisation...",
               "Préparation export rapport (simulé)...",
           ],
           "final": "💎 Téléchargez ce logiciel depuis la description du projet sur GitHub"},
    "de": {"name": "Deutsch", "start": "Scan Starten", "stop": "Stopp", "footer": "© 2025 FakeTools Studio",
           "tasks": [
               "Initialisiere Multi-Chain RPC (simuliert)...",
               "Lade Konfigurationen: ETH/BSC/Base/TRON/BTC...",
               "Prüfe Threads & Coroutines (virtuell)...",
               "Erzeuge zufällige Mnemonics (simuliert)...",
               "Simuliere Private-Key-Kollisionen...",
               "Simuliere paralleles Scannen (lokal)...",
               "Simuliere SQLite Deduplizierung...",
               "Prüfe Adressen und logge Treffer...",
               "Bereite Berichtsexport vor (simuliert)...",
           ],
           "final": "💎 Bitte laden Sie diese Software von der GitHub-Projektbeschreibung herunter"},
    "pt": {"name": "Português", "start": "Iniciar Varredura", "stop": "Parar", "footer": "© 2025 FakeTools Studio",
           "tasks": [
               "Inicializando RPC multi-chain (simulado)...",
               "Carregando configs: ETH/BSC/Base/TRON/BTC...",
               "Verificando threads e coroutines (virtual)...",
               "Gerando mnemônicos aleatórios (simulado)...",
               "Simulando colisão de chaves privadas...",
               "Simulando varredura paralela (local)...",
               "Simulando desduplicação SQLite...",
               "Verificando endereços e registrando hits...",
               "Preparando exportação de relatório (simulado)...",
           ],
           "final": "💎 Por favor, baixe este software na descrição do projeto no GitHub"},
    "it": {"name": "Italiano", "start": "Avvia Scansione", "stop": "Ferma", "footer": "© 2025 FakeTools Studio",
           "tasks": [
               "Inizializzo RPC multi-chain (simulato)...",
               "Carico config: ETH/BSC/Base/TRON/BTC...",
               "Controllo thread e coroutine (virtuale)...",
               "Genero mnemonic casuali (simulazione)...",
               "Simulo probabilità collisione chiavi private...",
               "Simulo scansione parallela (locale)...",
               "Simulo dedup SQLite...",
               "Verifico indirizzi e registro hit...",
               "Preparo esportazione report (simulato)...",
           ],
           "final": "💎 Scarica questo software dalla descrizione del progetto su GitHub"},
    # 可在此添加更多语言
}

# GUI 应用
class FakeScannerApp:
    def __init__(self, root):
        self.root = root
        self.lang = DEFAULT_LANG
        self.running = False

        root.title(APP_TITLE)
        root.geometry("760x520")
        root.configure(bg="#0f1720")

        header = tk.Label(root, text=APP_TITLE, fg="#7bed9f", bg="#0f1720",
                          font=("Segoe UI", 16, "bold"))
        header.pack(pady=(12, 6))

        # 顶部控制行：语言下拉 + 开始按钮
        ctrl_frame = tk.Frame(root, bg="#0f1720")
        ctrl_frame.pack(fill="x", padx=12)

        tk.Label(ctrl_frame, text="Language:", bg="#0f1720", fg="#bfe9d7").pack(side="left", padx=(0,6))
        self.lang_var = tk.StringVar(value=self.lang)
        lang_menu = ttk.Combobox(ctrl_frame, textvariable=self.lang_var, values=[f"{k} - {v['name']}" for k,v in LANGS.items()], state="readonly", width=28)
        lang_menu.pack(side="left")
        lang_menu.bind("<<ComboboxSelected>>", self.on_lang_change)

        self.start_btn = ttk.Button(ctrl_frame, text=LANGS[self.lang]["start"], command=self.toggle_scan)
        self.start_btn.pack(side="right", padx=6)

        # 主输出框
        self.output = tk.Text(root, bg="#071018", fg="#9ef0d8", insertbackground="#9ef0d8",
                              font=("Consolas", 11), padx=8, pady=8, wrap="word")
        self.output.pack(fill="both", expand=True, padx=12, pady=(8,6))

        # 进度条
        self.progress = ttk.Progressbar(root, orient="horizontal", length=660, mode="determinate")
        self.progress.pack(pady=(0,8))

        footer = tk.Label(root, text=LANGS[self.lang]["footer"], bg="#0f1720", fg="#688a7b", font=("Segoe UI", 9))
        footer.pack(side="bottom", pady=6)
        self.footer = footer

        # 自动写入初始欢迎
        self.print_welcome()

    def on_lang_change(self, _evt=None):
        sel = self.lang_var.get().split(" - ")[0]
        if sel in LANGS:
            self.lang = sel
            self.start_btn.config(text=LANGS[self.lang]["start"])
            self.footer.config(text=LANGS[self.lang]["footer"])
            self.print_welcome()

    def print_welcome(self):
        self.output.delete("1.0", "end")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"{APP_TITLE}\n{LANGS[self.lang]['name']} | {now}\n\n"
        self.output.insert("end", header)
        intro = {
            "zh": "此为演示界面，不进行任何真实的扫描或密钥操作。",
            "en": "This is a demo UI; no real scanning or key operations are performed.",
        }
        self.output.insert("end", intro.get(self.lang, intro["en"]) + "\n\n")
        self.output.insert("end", ">> " + LANGS[self.lang]["final"] + "\n\n")

    def toggle_scan(self):
        if self.running:
            # stop
            self.running = False
            self.start_btn.config(text=LANGS[self.lang]["start"])
            self.append_log("Scan stopped (simulated).")
        else:
            self.running = True
            self.start_btn.config(text=LANGS[self.lang]["stop"])
            threading.Thread(target=self.run_fake_scan, daemon=True).start()

    def append_log(self, text):
        self.output.insert("end", text + "\n")
        self.output.see("end")

    def run_fake_scan(self):
        tasks = LANGS[self.lang]["tasks"]
        total = len(tasks) + 3  # + final steps
        step = 0
        self.progress["value"] = 0
        self.output.delete("4.0", "end")  # 保留顶部欢迎
        for t in tasks:
            if not self.running:
                break
            self.append_log(f"[{step+1}/{total}] {t}")
            step += 1
            self.progress["value"] = int(step / total * 100)
            time.sleep(random.uniform(0.6, 1.2))
        # final simulated steps
        if self.running:
            for t in ["Finalizing (simulated)...", "Writing report (simulated)...", LANGS[self.lang]["final"]]:
                self.append_log(f"[{step+1}/{total}] {t}")
                step += 1
                self.progress["value"] = int(step / total * 100)
                time.sleep(random.uniform(0.5, 1.0))
        self.running = False
        self.start_btn.config(text=LANGS[self.lang]["start"])

def detect_default_lang():
    # 尝试根据系统环境设置默认语言（简单判断）
    import locale
    loc = locale.getdefaultlocale()[0] or ""
    for code in LANGS:
        if loc.lower().startswith(code):
            return code
    # zh/ja/ko mapping
    if loc.startswith("zh"):
        return "zh"
    if loc.startswith("ja"):
        return "ja"
    if loc.startswith("ko"):
        return "ko"
    return DEFAULT_LANG

if __name__ == "__main__":
    root = tk.Tk()
    DEFAULT_LANG = detect_default_lang()
    # ensure default present
    if DEFAULT_LANG not in LANGS:
        DEFAULT_LANG = "en"
    app = FakeScannerApp(root)
    # set combobox to default language value
    app.lang_var.set(f"{DEFAULT_LANG} - {LANGS[DEFAULT_LANG]['name']}")
    app.on_lang_change()
    root.mainloop()
