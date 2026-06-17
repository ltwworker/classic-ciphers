import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from encryption import caesar_cipher, vigenere_cipher, PolybiusCipher
from cryptanalysis import frequency_analysis, crack_caesar, calculate_ic, estimate_vigenere_key_length
from file_handler import load_file, save_file


class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Классические шифры и криптоанализ")
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        
        self.language = tk.StringVar(value='russian')
        self.mode = tk.StringVar(value='encrypt')
        self.algorithm = tk.StringVar(value='caesar')
        self.key_var = tk.StringVar()
        
        self._create_widgets()
        self._update_ui()
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(control_frame, text="Язык:").grid(row=0, column=0, padx=5, sticky='w')
        lang_combo = ttk.Combobox(control_frame, textvariable=self.language, 
                                  values=['russian', 'english'], state='readonly', width=10)
        lang_combo.grid(row=0, column=1, padx=5)
        lang_combo.bind('<<ComboboxSelected>>', lambda e: self._update_ui())
        
        ttk.Label(control_frame, text="Режим:").grid(row=0, column=2, padx=5, sticky='w')
        mode_combo = ttk.Combobox(control_frame, textvariable=self.mode,
                                  values=['encrypt', 'decrypt', 'cryptanalysis'], 
                                  state='readonly', width=15)
        mode_combo.grid(row=0, column=3, padx=5)
        mode_combo.bind('<<ComboboxSelected>>', lambda e: self._update_ui())
        
        ttk.Label(control_frame, text="Алгоритм:").grid(row=0, column=4, padx=5, sticky='w')
        algo_combo = ttk.Combobox(control_frame, textvariable=self.algorithm,
                                  values=['caesar', 'vigenere', 'polybius'],
                                  state='readonly', width=12)
        algo_combo.grid(row=0, column=5, padx=5)
        algo_combo.bind('<<ComboboxSelected>>', lambda e: self._update_ui())
        
        ttk.Label(control_frame, text="Ключ:").grid(row=0, column=6, padx=5, sticky='w')
        self.key_entry = ttk.Entry(control_frame, textvariable=self.key_var, width=15)
        self.key_entry.grid(row=0, column=7, padx=5)
        
        self.run_btn = ttk.Button(control_frame, text="Выполнить", command=self._run_operation)
        self.run_btn.grid(row=0, column=8, padx=10)
        
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        input_frame = ttk.LabelFrame(text_frame, text="Входной текст", padding="5")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=15, font=('Arial', 11))
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        self.input_text.bind('<Command-c>', lambda e: self.input_text.event_generate('<<Copy>>'))
        self.input_text.bind('<Command-v>', lambda e: self.input_text.event_generate('<<Paste>>'))
        self.input_text.bind('<Command-x>', lambda e: self.input_text.event_generate('<<Cut>>'))
        
        output_frame = ttk.LabelFrame(text_frame, text="Результат", padding="5")
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=15, font=('Arial', 11))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        self.output_text.bind('<Command-c>', lambda e: self.output_text.event_generate('<<Copy>>'))
        self.output_text.bind('<Command-v>', lambda e: self.output_text.event_generate('<<Paste>>'))
        self.output_text.bind('<Command-x>', lambda e: self.output_text.event_generate('<<Cut>>'))
        
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X)
        
        file_btn_frame = ttk.Frame(bottom_frame)
        file_btn_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(file_btn_frame, text="Загрузить файл", command=self._load_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_btn_frame, text="Сохранить файл", command=self._save_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_btn_frame, text="Очистить", command=self._clear_all).pack(side=tk.LEFT, padx=5)
        
        self.stats_frame = ttk.LabelFrame(bottom_frame, text="Статистика", padding="5")
        self.stats_frame.pack(side=tk.RIGHT, fill=tk.X, padx=(10, 0))
        self.stats_frame.pack_forget()
        
        self.freq_label = ttk.Label(self.stats_frame, text="Частоты: ")
        self.freq_label.pack(anchor='w')
        
        self.ic_label = ttk.Label(self.stats_frame, text="Индекс совпадений: ")
        self.ic_label.pack(anchor='w')
        
        self.key_len_label = ttk.Label(self.stats_frame, text="Длина ключа: ")
        self.key_len_label.pack(anchor='w')
        
        self.canvas_frame = ttk.LabelFrame(main_frame, text="Гистограмма частот", padding="5")
        self.canvas_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.canvas = tk.Canvas(self.canvas_frame, height=200, bg='white')
        self.canvas.pack(fill=tk.X)
    
    def _update_ui(self):
        mode = self.mode.get()
        algo = self.algorithm.get()
        
        if algo == 'polybius':
            self.key_entry.config(state='disabled')
            self.key_var.set('')
        else:
            self.key_entry.config(state='normal')
        
        if mode == 'cryptanalysis':
            self.stats_frame.pack(side=tk.RIGHT, fill=tk.X, padx=(10, 0))
        else:
            self.stats_frame.pack_forget()
        
        if mode == 'cryptanalysis':
            self.run_btn.config(text="Анализировать")
        else:
            self.run_btn.config(text="Выполнить")
    
    def _run_operation(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст для выполнения операции")
            return
        
        mode = self.mode.get()
        algo = self.algorithm.get()
        language = self.language.get()
        key = self.key_var.get().strip()
        
        try:
            if mode == 'cryptanalysis':
                self._run_cryptanalysis(text, language)
            else:
                self._run_cipher_operation(text, mode, algo, language, key)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    
    def _run_cipher_operation(self, text, mode, algo, language, key):
        is_encrypt = (mode == 'encrypt')
        result = ""
        
        if algo == 'caesar':
            try:
                shift = int(key) if key else 0
            except ValueError:
                messagebox.showerror("Ошибка", "Для шифра Цезаря ключ должен быть целым числом")
                return
            result = caesar_cipher(text, shift if is_encrypt else -shift, language)
            
        elif algo == 'vigenere':
            if not key or not key.isalpha():
                messagebox.showerror("Ошибка", "Для шифра Виженера ключ должен содержать только буквы")
                return
            result = vigenere_cipher(text, key, is_encrypt, language)
            
        elif algo == 'polybius':
            cipher = PolybiusCipher(language)
            if is_encrypt:
                result = cipher.encrypt(text)
            else:
                result = cipher.decrypt(text)
        
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)
    
    def _run_cryptanalysis(self, text, language):
        self.canvas.delete("all")
        
        freq = frequency_analysis(text, language)
        if freq:
            freq_str = ", ".join([f"{k}: {v}" for k, v in list(freq.items())[:10]])
            self.freq_label.config(text=f"Частоты (топ-10): {freq_str}")
            self._draw_histogram(freq)
        else:
            self.freq_label.config(text="Текст не содержит букв")
        
        ic = calculate_ic(text, language)
        if ic > 0.055:
            interpretation = "Текст похож на одноалфавитный или открытый"
        elif ic > 0.040:
            interpretation = "Возможно полиалфавитный шифр с коротким ключом"
        else:
            interpretation = "Текст похож на случайную последовательность"
        self.ic_label.config(text=f"Индекс совпадений: {ic:.4f} - {interpretation}")
        
        decrypted, shift = crack_caesar(text, language)
        if decrypted:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"=== Результат автоматического взлома шифра Цезаря ===\n")
            self.output_text.insert(tk.END, f"Предполагаемый ключ: {shift}\n\n")
            self.output_text.insert(tk.END, decrypted)
        else:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Не удалось выполнить взлом шифра Цезаря")
        
        key_len, score = estimate_vigenere_key_length(text, 20, language)
        self.key_len_label.config(text=f"Предполагаемая длина ключа Виженера: {key_len}")
    
    def _draw_histogram(self, freq):
        self.canvas.delete("all")
        if not freq:
            return
        
        max_freq = max(freq.values())
        bar_width = 22
        spacing = 6
        total_width = len(freq) * (bar_width + spacing)
        start_x = max(10, (self.canvas.winfo_width() - total_width) // 2)
        
        x = start_x
        for char, count in list(freq.items())[:30]:
            height = (count / max_freq) * 160
            self.canvas.create_rectangle(x, 180 - height, x + bar_width, 180, fill='steelblue', outline='navy')
            self.canvas.create_text(x + bar_width/2, 190, text=char, font=('Arial', 10))
            x += bar_width + spacing
    
    def _load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filepath:
            try:
                content = load_file(filepath)
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    def _save_file(self):
        content = self.output_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения")
            return
        
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            try:
                save_file(filepath, content)
                messagebox.showinfo("Успех", "Файл успешно сохранен")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    def _clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.canvas.delete("all")
        self.freq_label.config(text="Частоты: ")
        self.ic_label.config(text="Индекс совпадений: ")
        self.key_len_label.config(text="Длина ключа: ")


if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()