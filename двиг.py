import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import math

class FuturisticStepperMotorControl:
    def __init__(self, root):
        self.root = root
        self.root.title("УПРАВЛЕНИЕ ШАГОВЫМ ДВИГАТЕЛЕМ v2.0")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0a0a0a")
        
        # Цветовая схема футуристического дизайна
        self.colors = {
            "bg_dark": "#0a0a0a",
            "bg_medium": "#1a1a1a",
            "bg_light": "#2a2a2a",
            "accent_blue": "#00f3ff",
            "accent_purple": "#9d00ff",
            "accent_green": "#00ff9d",
            "accent_red": "#ff0066",
            "text_primary": "#ffffff",
            "text_secondary": "#aaaaaa",
            "glow_blue": (0, 243, 255, 0.3),
            "glow_purple": (157, 0, 255, 0.3)
        }
        
        # Параметры двигателя
        self.running = False
        self.direction = "CW"  # По часовой стрелке
        self.speed = 100  # шагов/сек
        self.current_step = 0
        self.total_steps = 0
        self.temperature = 42
        self.power = 120
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """Настройка кастомных стилей для виджетов"""
        style = ttk.Style()
        
        # Создаем свои стили
        style.theme_create("futuristic", parent="clam", settings={
            "TFrame": {
                "configure": {"background": self.colors["bg_dark"]}
            },
            "TLabel": {
                "configure": {
                    "background": self.colors["bg_dark"],
                    "foreground": self.colors["text_primary"],
                    "font": ("Segoe UI", 10)
                }
            },
            "TButton": {
                "configure": {
                    "background": self.colors["bg_light"],
                    "foreground": self.colors["text_primary"],
                    "borderwidth": 0,
                    "font": ("Segoe UI", 10, "bold"),
                    "padding": 10
                },
                "map": {
                    "background": [("active", self.colors["accent_blue"])],
                    "foreground": [("active", "#000000")]
                }
            },
            "TLabelFrame": {
                "configure": {
                    "background": self.colors["bg_medium"],
                    "foreground": self.colors["accent_blue"],
                    "relief": "flat",
                    "borderwidth": 1,
                    "font": ("Segoe UI", 11, "bold")
                }
            },
            "TScale": {
                "configure": {
                    "background": self.colors["bg_dark"],
                    "troughcolor": self.colors["bg_light"],
                    "borderwidth": 0,
                    "sliderlength": 30
                }
            },
            "TRadiobutton": {
                "configure": {
                    "background": self.colors["bg_medium"],
                    "foreground": self.colors["text_primary"],
                    "font": ("Segoe UI", 10)
                }
            }
        })
        
        style.theme_use("futuristic")
        
    def setup_ui(self):
        # Главный контейнер с сеткой
        main_container = tk.Frame(self.root, bg=self.colors["bg_dark"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Сетка 2x2
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=1)
        
        # Левая верхняя панель - Управление
        self.setup_control_panel(main_container)
        
        # Правая верхняя панель - Визуализация
        self.setup_visualization_panel(main_container)
        
        # Левая нижняя панель - Статистика
        self.setup_stats_panel(main_container)
        
        # Правая нижняя панель - Детали двигателя
        self.setup_details_panel(main_container)
        
    def setup_control_panel(self, parent):
        """Панель управления"""
        control_frame = tk.Frame(parent, bg=self.colors["bg_medium"], 
                                highlightbackground=self.colors["accent_blue"],
                                highlightthickness=1)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Заголовок с эффектом неона
        title_frame = tk.Frame(control_frame, bg=self.colors["bg_medium"])
        title_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(title_frame, text="ПАНЕЛЬ УПРАВЛЕНИЯ", 
                font=("Orbitron", 14, "bold"),
                bg=self.colors["bg_medium"],
                fg=self.colors["accent_blue"]).pack(side=tk.LEFT)
        
        # Разделитель
        self.create_separator(control_frame)
        
        # Скорость
        speed_frame = tk.Frame(control_frame, bg=self.colors["bg_medium"])
        speed_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(speed_frame, text="СКОРОСТЬ", 
                font=("Segoe UI", 10, "bold"),
                bg=self.colors["bg_medium"],
                fg=self.colors["text_secondary"]).pack(anchor=tk.W)
        
        self.speed_var = tk.IntVar(value=self.speed)
        speed_slider = tk.Scale(speed_frame, from_=1, to=500, 
                               variable=self.speed_var,
                               orient=tk.HORIZONTAL,
                               command=self.update_speed,
                               bg=self.colors["bg_medium"],
                               fg=self.colors["text_primary"],
                               troughcolor=self.colors["bg_light"],
                               highlightbackground=self.colors["bg_medium"],
                               activebackground=self.colors["accent_blue"],
                               sliderrelief="flat",
                               length=200)
        speed_slider.pack(fill=tk.X, pady=5)
        
        self.speed_label = tk.Label(speed_frame, 
                                   text=f"{self.speed} ШАГ/СЕК",
                                   font=("Consolas", 12, "bold"),
                                   bg=self.colors["bg_medium"],
                                   fg=self.colors["accent_green"])
        self.speed_label.pack()
        
        # Направление
        dir_frame = tk.Frame(control_frame, bg=self.colors["bg_medium"])
        dir_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(dir_frame, text="НАПРАВЛЕНИЕ",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors["bg_medium"],
                fg=self.colors["text_secondary"]).pack(anchor=tk.W)
        
        dir_btn_frame = tk.Frame(dir_frame, bg=self.colors["bg_medium"])
        dir_btn_frame.pack(fill=tk.X, pady=5)
        
        self.dir_var = tk.StringVar(value=self.direction)
        
        self.cw_btn = tk.Button(dir_btn_frame, text="ПО ЧАСОВОЙ",
                               font=("Segoe UI", 10, "bold"),
                               bg=self.colors["accent_blue"],
                               fg="#000000",
                               relief="flat",
                               padx=20,
                               command=lambda: self.set_direction("CW"))
        self.cw_btn.pack(side=tk.LEFT, padx=2)
        
        self.ccw_btn = tk.Button(dir_btn_frame, text="ПРОТИВ ЧАСОВОЙ",
                                font=("Segoe UI", 10, "bold"),
                                bg=self.colors["bg_light"],
                                fg=self.colors["text_primary"],
                                relief="flat",
                                padx=20,
                                command=lambda: self.set_direction("CCW"))
        self.ccw_btn.pack(side=tk.RIGHT, padx=2)
        
        # Основные кнопки управления
        btn_frame = tk.Frame(control_frame, bg=self.colors["bg_medium"])
        btn_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.start_btn = self.create_futuristic_button(btn_frame, "▶ ЗАПУСК", 
                                                      self.colors["accent_green"], 
                                                      self.start_motor)
        self.start_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.stop_btn = self.create_futuristic_button(btn_frame, "⏹ СТОП", 
                                                     self.colors["accent_red"], 
                                                     self.stop_motor, 
                                                     state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.reset_btn = self.create_futuristic_button(btn_frame, "↻ СБРОС", 
                                                      self.colors["accent_blue"], 
                                                      self.reset_motor)
        self.reset_btn.pack(side=tk.LEFT, padx=5, expand=True)
        
    def setup_visualization_panel(self, parent):
        """Панель визуализации двигателя"""
        viz_frame = tk.Frame(parent, bg=self.colors["bg_medium"],
                            highlightbackground=self.colors["accent_purple"],
                            highlightthickness=1)
        viz_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Заголовок
        title_frame = tk.Frame(viz_frame, bg=self.colors["bg_medium"])
        title_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(title_frame, text="ВИЗУАЛИЗАЦИЯ ДВИГАТЕЛЯ", 
                font=("Orbitron", 14, "bold"),
                bg=self.colors["bg_medium"],
                fg=self.colors["accent_purple"]).pack(side=tk.LEFT)
        
        # Canvas для анимации
        self.canvas = tk.Canvas(viz_frame, width=500, height=350, 
                               bg=self.colors["bg_dark"],
                               highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Инициализация анимации
        self.setup_motor_animation()
        
    def setup_motor_animation(self):
        """Настройка анимированного двигателя"""
        self.center_x = 250
        self.center_y = 175
        self.radius = 120
        
        # Внешнее кольцо с эффектом свечения
        self.canvas.create_oval(self.center_x - self.radius - 10, 
                               self.center_y - self.radius - 10,
                               self.center_x + self.radius + 10, 
                               self.center_y + self.radius + 10,
                               outline=self.colors["accent_purple"],
                               width=2, tags="glow")
        
        # Корпус двигателя
        self.canvas.create_oval(self.center_x - self.radius, 
                               self.center_y - self.radius,
                               self.center_x + self.radius, 
                               self.center_y + self.radius,
                               fill=self.colors["bg_light"],
                               outline=self.colors["accent_blue"],
                               width=2, tags="housing")
        
        # Внутренняя область
        self.canvas.create_oval(self.center_x - self.radius + 20, 
                               self.center_y - self.radius + 20,
                               self.center_x + self.radius - 20, 
                               self.center_y + self.radius - 20,
                               fill=self.colors["bg_dark"],
                               outline=self.colors["accent_blue"],
                               width=1, tags="inner")
        
        # Статорные катушки (4 штуки)
        self.coils = []
        for i in range(4):
            angle = i * 90
            x = self.center_x + (self.radius * 0.6) * math.cos(math.radians(angle))
            y = self.center_y + (self.radius * 0.6) * math.sin(math.radians(angle))
            
            coil = self.canvas.create_oval(x-15, y-15, x+15, y+15,
                                          fill=self.colors["bg_light"],
                                          outline=self.colors["accent_blue"],
                                          width=2, tags=f"coil_{i}")
            self.coils.append(coil)
            
            # Текстовые метки
            label_x = self.center_x + (self.radius * 0.8) * math.cos(math.radians(angle))
            label_y = self.center_y + (self.radius * 0.8) * math.sin(math.radians(angle))
            self.canvas.create_text(label_x, label_y, text=f"КАТУШКА {i+1}",
                                   fill=self.colors["text_secondary"],
                                   font=("Segoe UI", 8), tags=f"label_{i}")
        
        # Ротор (будет вращаться)
        self.rotor = self.canvas.create_oval(self.center_x - 70, self.center_y - 70,
                                            self.center_x + 70, self.center_y + 70,
                                            fill="#1a2a3a",
                                            outline=self.colors["accent_green"],
                                            width=2, tags="rotor")
        
        # Магниты на роторе
        self.magnets = []
        for i in range(8):
            angle = i * 45
            x = self.center_x + 50 * math.cos(math.radians(angle))
            y = self.center_y + 50 * math.sin(math.radians(angle))
            
            color = self.colors["accent_red"] if i % 2 == 0 else self.colors["accent_blue"]
            magnet = self.canvas.create_oval(x-8, y-8, x+8, y+8,
                                            fill=color,
                                            outline="white",
                                            width=1, tags=f"magnet_{i}")
            self.magnets.append(magnet)
        
        # Центральный вал
        self.canvas.create_oval(self.center_x - 10, self.center_y - 10,
                               self.center_x + 10, self.center_y + 10,
                               fill=self.colors["text_primary"],
                               outline=self.colors["accent_green"],
                               width=2, tags="shaft")
        
        # Индикатор шага
        self.step_indicator = self.canvas.create_oval(self.center_x - 5, 
                                                     self.center_y - self.radius + 5,
                                                     self.center_x + 5, 
                                                     self.center_y - self.radius + 15,
                                                     fill=self.colors["accent_green"],
                                                     outline="", tags="indicator")
        
    def setup_stats_panel(self, parent):
        """Панель статистики"""
        stats_frame = tk.Frame(parent, bg=self.colors["bg_medium"],
                              highlightbackground=self.colors["accent_green"],
                              highlightthickness=1)
        stats_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Заголовок
        tk.Label(stats_frame, text="СТАТИСТИКА СИСТЕМЫ", 
                font=("Orbitron", 14, "bold"),
                bg=self.colors["bg_medium"],
                fg=self.colors["accent_green"]).pack(pady=15)
        
        # Контейнер для статистики
        stats_container = tk.Frame(stats_frame, bg=self.colors["bg_medium"])
        stats_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Метрики
        metrics = [
            ("ПОЗИЦИЯ", "0", "шагов"),
            ("ВСЕГО ШАГОВ", "0", "шагов"),
            ("СКОРОСТЬ", "100", "шаг/сек"),
            ("ТЕМПЕРАТУРА", "42", "°C"),
            ("МОЩНОСТЬ", "120", "Вт"),
            ("МОМЕНТ", "75", "%")
        ]
        
        self.metric_labels = {}
        
        for i, (name, value, unit) in enumerate(metrics):
            metric_frame = tk.Frame(stats_container, bg=self.colors["bg_medium"])
            metric_frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
            
            # Название метрики
            tk.Label(metric_frame, text=name,
                    font=("Segoe UI", 9),
                    bg=self.colors["bg_medium"],
                    fg=self.colors["text_secondary"]).pack(anchor=tk.W)
            
            # Значение метрики
            value_label = tk.Label(metric_frame, text=value,
                                  font=("Consolas", 16, "bold"),
                                  bg=self.colors["bg_medium"],
                                  fg=self.colors["accent_blue"])
            value_label.pack(anchor=tk.W)
            
            # Единица измерения
            tk.Label(metric_frame, text=unit,
                    font=("Segoe UI", 8),
                    bg=self.colors["bg_medium"],
                    fg=self.colors["text_secondary"]).pack(anchor=tk.W)
            
            self.metric_labels[name] = value_label
        
        # Разделитель
        self.create_separator(stats_frame)
        
        # Кнопки шагового управления
        step_frame = tk.Frame(stats_frame, bg=self.colors["bg_medium"])
        step_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(step_frame, text="ШАГОВОЕ УПРАВЛЕНИЕ",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors["bg_medium"],
                fg=self.colors["text_secondary"]).pack(anchor=tk.W, pady=5)
        
        step_btn_frame = tk.Frame(step_frame, bg=self.colors["bg_medium"])
        step_btn_frame.pack(fill=tk.X)
        
        tk.Button(step_btn_frame, text="+1 ШАГ", 
                 command=lambda: self.step_motor(1),
                 **self.get_button_style(self.colors["bg_light"])).pack(side=tk.LEFT, padx=2, expand=True)
        
        tk.Button(step_btn_frame, text="-1 ШАГ",
                 command=lambda: self.step_motor(-1),
                 **self.get_button_style(self.colors["bg_light"])).pack(side=tk.LEFT, padx=2, expand=True)
        
        tk.Button(step_btn_frame, text="+10 ШАГОВ",
                 command=lambda: self.step_motor(10),
                 **self.get_button_style(self.colors["accent_blue"])).pack(side=tk.LEFT, padx=2, expand=True)
        
        tk.Button(step_btn_frame, text="-10 ШАГОВ",
                 command=lambda: self.step_motor(-10),
                 **self.get_button_style(self.colors["accent_blue"])).pack(side=tk.LEFT, padx=2, expand=True)
        
    def setup_details_panel(self, parent):
        """Панель деталей и состояния"""
        details_frame = tk.Frame(parent, bg=self.colors["bg_medium"],
                                highlightbackground=self.colors["accent_red"],
                                highlightthickness=1)
        details_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Заголовок
        tk.Label(details_frame, text="СОСТОЯНИЕ ДВИГАТЕЛЯ", 
                font=("Orbitron", 14, "bold"),
                bg=self.colors["bg_medium"],
                fg=self.colors["accent_red"]).pack(pady=15)
        
        # Индикатор состояния
        status_frame = tk.Frame(details_frame, bg=self.colors["bg_medium"])
        status_frame.pack(pady=20)
        
        self.status_indicator = tk.Canvas(status_frame, width=200, height=40,
                                         bg=self.colors["bg_medium"],
                                         highlightthickness=0)
        self.status_indicator.pack()
        
        self.status_text = tk.Label(status_frame, text="СИСТЕМА: ОЖИДАНИЕ",
                                   font=("Consolas", 12, "bold"),
                                   bg=self.colors["bg_medium"],
                                   fg=self.colors["accent_red"])
        self.status_text.pack()
        
        self.update_status_indicator("ОЖИДАНИЕ")
        
        # Прогресс-бары
        progress_frame = tk.Frame(details_frame, bg=self.colors["bg_medium"])
        progress_frame.pack(fill=tk.X, padx=30, pady=20)
        
        # Температура
        tk.Label(progress_frame, text="ТЕМПЕРАТУРА",
                font=("Segoe UI", 9),
                bg=self.colors["bg_medium"],
                fg=self.colors["text_secondary"]).pack(anchor=tk.W)
        
        self.temp_bar = self.create_progress_bar(progress_frame, self.colors["accent_red"])
        
        # Загрузка
        tk.Label(progress_frame, text="НАГРУЗКА",
                font=("Segoe UI", 9),
                bg=self.colors["bg_medium"],
                fg=self.colors["text_secondary"]).pack(anchor=tk.W, pady=(15, 0))
        
        self.load_bar = self.create_progress_bar(progress_frame, self.colors["accent_blue"])
        
        # Информация о системе
        info_frame = tk.Frame(details_frame, bg=self.colors["bg_medium"])
        info_frame.pack(fill=tk.X, padx=30, pady=20)
        
        info_text = """
        СИСТЕМА: ШАГОВЫЙ ДВИГАТЕЛЬ v2.0
        РЕЖИМ: ПОЛНЫЙ ШАГ
        ДРАЙВЕР: БИПОЛЯРНЫЙ
        РАЗРЕШЕНИЕ: 1.8°
        МАКС. СКОРОСТЬ: 500 ШАГ/СЕК
        """
        
        tk.Label(info_frame, text=info_text.strip(),
                font=("Consolas", 9),
                bg=self.colors["bg_medium"],
                fg=self.colors["text_secondary"],
                justify=tk.LEFT).pack(anchor=tk.W)
        
    def create_futuristic_button(self, parent, text, color, command, state=tk.NORMAL):
        """Создание кнопки в футуристическом стиле"""
        btn = tk.Button(parent, text=text,
                       font=("Segoe UI", 10, "bold"),
                       bg=color,
                       fg="#000000" if color in [self.colors["accent_blue"], 
                                                self.colors["accent_green"]] else "#ffffff",
                       relief="flat",
                       padx=20,
                       pady=8,
                       command=command,
                       state=state,
                       cursor="hand2")
        
        # Эффект при наведении
        btn.bind("<Enter>", lambda e: btn.config(bg=self.lighten_color(color, 20)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        
        return btn
    
    def get_button_style(self, color):
        """Возвращает стиль для кнопки"""
        return {
            "font": ("Segoe UI", 9, "bold"),
            "bg": color,
            "fg": self.colors["text_primary"],
            "relief": "flat",
            "padx": 10,
            "pady": 5,
            "cursor": "hand2"
        }
    
    def create_separator(self, parent):
        """Создание стильного разделителя"""
        sep = tk.Frame(parent, height=1, bg=self.colors["accent_blue"])
        sep.pack(fill=tk.X, padx=20, pady=10)
        return sep
    
    def create_progress_bar(self, parent, color):
        """Создание прогресс-бара в футуристическом стиле"""
        frame = tk.Frame(parent, bg=self.colors["bg_light"], height=15)
        frame.pack(fill=tk.X, pady=5)
        
        # Внутренний бар
        inner = tk.Frame(frame, bg=color, height=13)
        inner.place(relx=0, rely=0.07, relwidth=0.5, relheight=0.86)
        
        return inner
    
    def update_progress_bar(self, bar, value):
        """Обновление прогресс-бара"""
        bar.place(relx=0, rely=0.07, relwidth=value/100, relheight=0.86)
    
    def update_status_indicator(self, status):
        """Обновление индикатора состояния"""
        self.status_indicator.delete("all")
        
        colors = {
            "ОЖИДАНИЕ": self.colors["accent_red"],
            "РАБОТАЕТ": self.colors["accent_green"],
            "ОШИБКА": self.colors["accent_red"]
        }
        
        color = colors.get(status, self.colors["accent_blue"])
        
        # Рисуем индикатор
        self.status_indicator.create_rectangle(10, 10, 190, 30,
                                              fill=self.colors["bg_light"],
                                              outline=color,
                                              width=2)
        
        # Анимированный индикатор
        if status == "РАБОТАЕТ":
            for i in range(3):
                x = 30 + i * 50
                self.status_indicator.create_oval(x, 15, x+10, 25,
                                                 fill=color,
                                                 outline="",
                                                 tags=f"pulse_{i}")
            self.pulse_animation()
        else:
            self.status_indicator.create_oval(30, 15, 40, 25,
                                             fill=color,
                                             outline="")
    
    def pulse_animation(self):
        """Анимация пульсации для индикатора"""
        if self.running:
            for i in range(3):
                alpha = 0.3 + 0.7 * abs(math.sin(time.time() * 2 + i))
                color = self.blend_colors(self.colors["accent_green"], "#ffffff", alpha)
                self.status_indicator.itemconfig(f"pulse_{i}", fill=color)
            
            self.root.after(100, self.pulse_animation)
    
    def update_speed(self, event=None):
        """Обновление скорости"""
        self.speed = self.speed_var.get()
        self.speed_label.config(text=f"{self.speed} ШАГ/СЕК")
        self.metric_labels["СКОРОСТЬ"].config(text=str(self.speed))
    
    def set_direction(self, direction):
        """Установка направления"""
        self.direction = direction
        
        if direction == "CW":
            self.cw_btn.config(bg=self.colors["accent_blue"], fg="#000000")
            self.ccw_btn.config(bg=self.colors["bg_light"], fg=self.colors["text_primary"])
        else:
            self.cw_btn.config(bg=self.colors["bg_light"], fg=self.colors["text_primary"])
            self.ccw_btn.config(bg=self.colors["accent_blue"], fg="#000000")
    
    def start_motor(self):
        """Запуск двигателя"""
        if not self.running:
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.status_text.config(text="СИСТЕМА: РАБОТАЕТ", fg=self.colors["accent_green"])
            self.update_status_indicator("РАБОТАЕТ")
            
            # Запуск анимации
            self.animation_thread = threading.Thread(target=self.animate_motor, daemon=True)
            self.animation_thread.start()
    
    def stop_motor(self):
        """Остановка двигателя"""
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        self.status_text.config(text="СИСТЕМА: ОЖИДАНИЕ", fg=self.colors["accent_red"])
        self.update_status_indicator("ОЖИДАНИЕ")
    
    def reset_motor(self):
        """Сброс двигателя"""
        self.stop_motor()
        self.current_step = 0
        self.total_steps = 0
        self.update_display()
        self.rotate_motor(0)
    
    def step_motor(self, steps):
        """Шаговое управление"""
        if not self.running:
            self.current_step += steps
            self.total_steps += abs(steps)
            self.update_display()
            self.rotate_motor(self.current_step * 1.8)
    
    def animate_motor(self):
        """Анимация работы двигателя"""
        step_delay = 1.0 / self.speed
        
        while self.running:
            step = 1 if self.direction == "CW" else -1
            self.current_step += step
            self.total_steps += 1
            
            # Обновление интерфейса
            self.root.after(0, self.update_display)
            self.root.after(0, lambda: self.rotate_motor(self.current_step * 1.8))
            
            # Обновление температуры и мощности (имитация)
            self.temperature = min(100, 42 + self.speed // 20 + self.total_steps // 1000)
            self.power = 120 + self.speed // 5
            
            self.root.after(0, self.update_system_stats)
            
            time.sleep(step_delay)
    
    def rotate_motor(self, angle_deg):
        """Вращение ротора"""
        # Поворачиваем магниты
        for i, magnet in enumerate(self.magnets):
            original_angle = i * 45
            new_angle = original_angle + angle_deg
            x = self.center_x + 50 * math.cos(math.radians(new_angle))
            y = self.center_y + 50 * math.sin(math.radians(new_angle))
            
            coords = self.canvas.coords(magnet)
            width = coords[2] - coords[0]
            height = coords[3] - coords[1]
            
            self.canvas.coords(magnet, 
                             x - width/2, y - height/2,
                             x + width/2, y + height/2)
        
        # Обновляем подсветку катушек
        active_coil = (self.current_step // 2) % 4
        for i, coil in enumerate(self.coils):
            if i == active_coil:
                self.canvas.itemconfig(coil, fill=self.colors["accent_green"])
            else:
                self.canvas.itemconfig(coil, fill=self.colors["bg_light"])
        
        # Перемещаем индикатор шага
        indicator_angle = angle_deg
        x = self.center_x + (self.radius - 10) * math.cos(math.radians(indicator_angle))
        y = self.center_y + (self.radius - 10) * math.sin(math.radians(indicator_angle))
        
        coords = self.canvas.coords(self.step_indicator)
        width = coords[2] - coords[0]
        height = coords[3] - coords[1]
        
        self.canvas.coords(self.step_indicator,
                          x - width/2, y - height/2,
                          x + width/2, y + height/2)
        
        self.canvas.update()
    
    def update_display(self):
        """Обновление отображения"""
        self.metric_labels["ПОЗИЦИЯ"].config(text=str(self.current_step))
        self.metric_labels["ВСЕГО ШАГОВ"].config(text=str(self.total_steps))
    
    def update_system_stats(self):
        """Обновление системной статистики"""
        self.metric_labels["ТЕМПЕРАТУРА"].config(text=str(self.temperature))
        self.metric_labels["МОЩНОСТЬ"].config(text=str(self.power))
        
        # Обновляем прогресс-бары
        self.update_progress_bar(self.temp_bar, self.temperature)
        self.update_progress_bar(self.load_bar, min(100, self.speed // 5))
        
        # Обновляем метрику крутящего момента
        torque = min(100, 75 + self.speed // 20)
        self.metric_labels["МОМЕНТ"].config(text=str(torque))
    
    @staticmethod
    def lighten_color(color, amount):
        """Осветление цвета"""
        if color.startswith("#"):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            r = min(255, r + amount)
            g = min(255, g + amount)
            b = min(255, b + amount)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    @staticmethod
    def blend_colors(color1, color2, alpha):
        """Смешивание двух цветов"""
        if color1.startswith("#"):
            r1 = int(color1[1:3], 16)
            g1 = int(color1[3:5], 16)
            b1 = int(color1[5:7], 16)
        else:
            return color1
        
        if color2.startswith("#"):
            r2 = int(color2[1:3], 16)
            g2 = int(color2[3:5], 16)
            b2 = int(color2[5:7], 16)
        else:
            return color1
        
        r = int(r1 * alpha + r2 * (1 - alpha))
        g = int(g1 * alpha + g2 * (1 - alpha))
        b = int(b1 * alpha + b2 * (1 - alpha))
        
        return f"#{r:02x}{g:02x}{b:02x}"

def main():
    root = tk.Tk()
    
    try:
        icon = tk.PhotoImage(file='image.png')
        root.iconphoto(True, icon)
    except:
        pass
    
    app = FuturisticStepperMotorControl(root)
    
    # Центрируем окно
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()