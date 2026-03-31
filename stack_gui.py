import ctypes
import ctypes.util
from tkinter import *
from tkinter import messagebox, ttk
import os
import sys




class StackWrapper:
    def __init__(self, lib_path, lib_name):
        self.lib_name = lib_name
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Библиотека {lib_path} не найдена")
        
        self.lib = ctypes.CDLL(lib_path)
        self.stack_ptr = None
        
        self._setup_functions()
        self.stack_ptr = self.lib.create_stack()
    def _setup_functions(self):
        funcs_setup = [
            ('create_stack', [], ctypes.c_void_p),
            ('delete_stack', [ctypes.c_void_p], None),
            ('is_empty', [ctypes.c_void_p], ctypes.c_int),
            ('push', [ctypes.c_void_p, ctypes.c_int], ctypes.c_int),
            ('pop', [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)], ctypes.c_int),
            ('peek', [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)], ctypes.c_int),
            ('get_size', [ctypes.c_void_p], ctypes.c_int),
            ('clear_stack', [ctypes.c_void_p], None),
            ('get_all_elements', [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)], ctypes.POINTER(ctypes.c_int)),
            ('free_elements', [ctypes.POINTER(ctypes.c_int)], None),
        ]
        
        for func_name, argtypes, restype in funcs_setup:
            try:
                func = getattr(self.lib, func_name)
                func.argtypes = argtypes
                func.restype = restype
            except AttributeError:
                pass
    
    def __del__(self):
        if hasattr(self, 'stack_ptr') and self.stack_ptr:
            try:
                self.lib.delete_stack(self.stack_ptr)
            except:
                pass
    
    def push(self, value):
        result = self.lib.push(self.stack_ptr, value)
        return result == 0
    
    def pop(self):
        result = ctypes.c_int()
        err = self.lib.pop(self.stack_ptr, ctypes.byref(result))
        if err != 0:
            raise IndexError("Стек пуст")
        return result.value
    
    def peek(self):
        result = ctypes.c_int()
        err = self.lib.peek(self.stack_ptr, ctypes.byref(result))
        if err != 0:
            raise IndexError("Стек пуст")
        return result.value
    
    def is_empty(self):
        return bool(self.lib.is_empty(self.stack_ptr))
    
    def size(self):
        return int(self.lib.get_size(self.stack_ptr))
    
    def get_all(self):
        size = ctypes.c_int()
        elements_ptr = self.lib.get_all_elements(
            self.stack_ptr, ctypes.byref(size))
        
        if not elements_ptr or size.value == 0:
            return []
        
        elements = [elements_ptr[i] for i in range(size.value)]
        self.lib.free_elements(elements_ptr)
        return elements
    
    def clear(self):
        self.lib.clear_stack(self.stack_ptr)


class StackLibraryManager:
    LIBRARIES = {
        "C": {
            "name": "C",
            "win": "stack.dll",
            "linux": "libstack.so",
            "mac": "libstack.dylib"
        },
        "C++": {
            "name": "C++",
            "win": "stack_cpp.dll",
            "linux": "libstack_cpp.so",
            "mac": "libstack_cpp.dylib"
        },
        "Pascal": {
            "name": "Pascal",
            "win": "libstack_cpp.dll",
            "linux": "libstack_cpp.so",
            "mac": "libstack_cpp.dylib"
        }

    }

    def __init__(self):
        self.stack = None
        self.current_lang = None

    def load_library(self, lang):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))

            if lang == "Python":
                import libstack_py
                self.stack = libstack_py.Stack()
                self.current_lang = lang
                return True, f"Python библиотека загружена"

            else:
                lib_info = self.LIBRARIES[lang]

                if sys.platform == "win32":
                    lib_file = lib_info["win"]
                elif sys.platform == "darwin":
                    lib_file = lib_info["mac"]
                else:
                    lib_file = lib_info["linux"]

                lib_path = os.path.join(script_dir, lib_file)
                self.stack = StackWrapper(lib_path, lang)
                self.current_lang = lang
                return True, f"Библиотека {lang} загружена"

        except Exception as e:
            return False, str(e)

    def unload_library(self):
        self.stack = None
        self.current_lang = None

    def current_lang(self):
        return self.current_lang


class ModernStackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("STACK MANAGER - Multilanguage Edition")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.library_manager = StackLibraryManager()
        self.lang_var = StringVar(value="C")
        
        self.setup_styles()
        self.create_widgets()
        self.update_display()
        
        self.load_selected_library()
    
    def setup_styles(self):
        self.theme = {
            'bg': '#1a1a2e',
            'panel': '#16213e',
            'accent': '#0f3460',
            'primary': '#e94560',
            'success': '#4cc9f0',
            'warning': '#f72585',
            'info': '#4361ee',
            'text_main': '#ffffff',
            'text_secondary': '#a0a0a0',
            'border': '#303040'
        }
        self.root.configure(bg=self.theme['bg'])
    
    def create_widgets(self):
        self.create_header_section()
        self.create_main_area()
        self.create_status_panel()
    
    def create_header_section(self):
        header_frame = Frame(self.root, bg=self.theme['panel'], padx=20, pady=15)
        header_frame.pack(fill=X, side=TOP)
        
        title_label = Label(
            header_frame, 
            text="STACK MANAGER - MULTILANGUAGE",
            font=("Arial", 18, "bold"),
            fg=self.theme['text_main'],
            bg=self.theme['panel']
        )
        title_label.pack(side=LEFT)
        
        selector_frame = Frame(header_frame, bg=self.theme['panel'])
        selector_frame.pack(side=RIGHT)
        
        Button(selector_frame, text="C", width=5, height=1,
                command=lambda l="C": self.switch_to_language(l),
                bg=self.theme['accent'], fg='white',
                activebackground=self.theme['primary'],
                font=("Arial", 10, "bold")).pack(side=LEFT, padx=3)
        
        Button(selector_frame, text="C++", width=5, height=1,
                command=lambda l="C++": self.switch_to_language(l),
                bg=self.theme['accent'], fg='white',
                activebackground=self.theme['primary'],
                font=("Arial", 10, "bold")).pack(side=LEFT, padx=3)
        
        Button(selector_frame, text="Pascal", width=7, height=1,
                command=lambda l="Pascal": self.switch_to_language(l),
                bg=self.theme['accent'], fg='white',
                activebackground=self.theme['primary'],
                font=("Arial", 10, "bold")).pack(side=LEFT, padx=3)
        Button(selector_frame, text="Python", width=7, height=1,
                command=lambda l="Python": self.switch_to_language(l),
                bg=self.theme['accent'], fg='white',
                activebackground=self.theme['primary'],
                font=("Arial", 10, "bold")).pack(side=LEFT, padx=3)

    def create_main_area(self):
        main_container = Frame(self.root, bg=self.theme['bg'])
        main_container.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        left_panel = Frame(main_container, bg=self.theme['panel'], relief=SUNKEN, bd=1)
        left_panel.pack(side=LEFT, fill=Y, padx=(0, 10))
        
        right_panel = Frame(main_container, bg=self.theme['panel'], relief=SUNKEN, bd=1)
        right_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0))
        
        self.create_control_panel(left_panel)
        self.create_display_panel(right_panel)
    
    def create_control_panel(self, parent):
        frame_title = Label(parent, text="Operations (Операции)", 
                           font=("Arial", 12, "bold"), 
                           fg=self.theme['success'], bg=self.theme['panel'])
        frame_title.pack(pady=10, padx=10, anchor=W)
        
        input_frame = Frame(parent, bg=self.theme['panel'])
        input_frame.pack(fill=X, padx=10, pady=5)
        
        Label(input_frame, text="Enter Value (Значение):", 
              font=("Arial", 10), fg=self.theme['text_secondary']).pack(anchor=W)
        
        self.entry_value = Entry(input_frame, font=("Consolas", 12), 
                                bg='#2d2d44', fg='white', relief=GROOVE)
        self.entry_value.pack(fill=X, padx=5, pady=5)
        self.entry_value.bind('<Return>', lambda e: self.execute_push())
        
        action_buttons = [
            ("Push (Добавить)", self.execute_push, self.theme['success']),
            ("Pop (Удалить)", self.execute_pop, self.theme['warning']),
            ("Peek (Вершина)", self.execute_peek, self.theme['info']),
        ]
        
        for text, cmd, color in action_buttons:
            btn = Button(parent, text=text, command=cmd,
                        bg=color, fg='white', font=("Arial", 11, "bold"),
                        height=2, activebackground=self.theme['primary'],
                        relief=RAISED, borderwidth=2)
            btn.pack(fill=X, padx=10, pady=5)
        
        extra_frame = Frame(parent, bg=self.theme['panel'])
        extra_frame.pack(fill=X, padx=10, pady=15)
        
        extra_buttons = [
            ("Check Empty (Проверка)", self.check_empty, self.theme['accent']),
            ("Clear Stack (Очистить)", self.clear_stack, self.theme['primary']),
            ("Show Size (Размер)", self.show_size, self.theme['accent']),
        ]
        
        for text, cmd, color in extra_buttons:
            btn = Button(extra_frame, text=text, command=cmd,
                        bg=color, fg='white', font=("Arial", 9),
                        height=1, relief=FLAT, activebackground=self.theme['primary'])
            btn.pack(fill=X, padx=5, pady=2)
    
    def create_display_panel(self, parent):
        display_title = Label(parent, text="Stack (Содержимое)", 
                             font=("Arial", 12, "bold"), 
                             fg=self.theme['primary'], bg=self.theme['panel'])
        display_title.pack(pady=10, padx=10, anchor=W)
        
        canvas_container = Frame(parent, bg=self.theme['panel'])
        canvas_container.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        self.canvas = Canvas(canvas_container, bg=self.theme['bg'], 
                            highlightthickness=0)
        scrollbar = Scrollbar(canvas_container, orient=VERTICAL, 
                             command=self.canvas.yview)
        
        self.scrollable_frame = Frame(self.canvas, bg=self.theme['bg'])
        self.canvas_window = self.canvas.create_window((0, 0), 
                                                      window=self.scrollable_frame,
                                                      anchor='nw')
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.scrollable_frame.bind('<Configure>', self.on_frame_configure)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
    
    def create_status_panel(self):
        status_bar = Frame(self.root, bg=self.theme['panel'], relief=SUNKEN, bd=1)
        status_bar.pack(fill=X, side=BOTTOM)
        
        self.status_label = Label(status_bar, text="Готов к работе", 
                                 font=("Arial", 10), fg=self.theme['success'],
                                 bg=self.theme['panel'], anchor=W)
        self.status_label.pack(side=LEFT, padx=10, pady=5)
        
        self.lang_label = Label(status_bar, text="Версия: C", 
                               font=("Arial", 10), fg=self.theme['text_secondary'],
                               bg=self.theme['panel'], anchor=E)
        self.lang_label.pack(side=RIGHT, padx=10, pady=5)
    
    def load_selected_library(self):
        lang = self.lang_var.get()
        success, msg = self.library_manager.load_library(lang)
        
        if success:
            self.status_label.config(text=msg, fg=self.theme['success'])
            self.lang_label.config(text=f"Версия: {lang}")
            self.update_display()
        else:
            self.status_label.config(text=f"Ошибка: {msg}", fg=self.theme['warning'])
            messagebox.showerror("Ошибка загрузки", msg)
    
    def switch_to_language(self, lang):
        if messagebox.askyesno("Подтверждение", 
                              f"Сменить библиотеку на {lang}? \nТекущие данные будут потеряны."):
            self.library_manager.unload_library()
            self.lang_var.set(lang)
            self.load_selected_library()
    
    def execute_push(self):
        try:
            value_str = self.entry_value.get().strip()
            if not value_str:
                raise ValueError("Поле ввода пустое")
            
            value = int(value_str)
            if self.library_manager.stack.push(value):
                self.entry_value.delete(0, END)
                self.show_message(f"Добавлено: {value}", 'success')
                self.update_display()
            else:
                raise RuntimeError("Ошибка при добавлении")
                
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def execute_pop(self):
        try:
            value = self.library_manager.stack.pop()
            self.show_message(f"Удалено: {value}", 'success')
            self.update_display()
        except IndexError:
            self.show_message("Стек пуст", 'warning')
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def execute_peek(self):
        try:
            value = self.library_manager.stack.peek()
            self.show_message(f"Верхний элемент: {value}", 'info')
        except IndexError:
            self.show_message("Стек пуст", 'warning')
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def check_empty(self):
        is_empty = self.library_manager.stack.is_empty()
        count = self.library_manager.stack.size()
        msg = "Стек пуст" if is_empty else f"Элементов: {count}"
        self.show_message(msg, 'info' if is_empty else 'success')
    
    def clear_stack(self):
        if messagebox.askyesno("Подтверждение", "Очистить весь стек?"):
            self.library_manager.stack.clear()
            self.show_message("Стек очищен", 'success')
            self.update_display()
    
    def show_size(self):
        size = self.library_manager.stack.size()
        self.show_message(f"Размер стека: {size}", 'info')
    
    def update_display(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        try:
            elements = self.library_manager.stack.get_all()
            size = self.library_manager.stack.size()
            
            if size == 0:
                Label(self.scrollable_frame, text="Пусто", 
                      font=("Arial", 14), fg=self.theme['text_secondary'],
                      bg=self.theme['bg']).pack(pady=40)
            else:
                for i, value in enumerate(elements):
                    is_top = (i == len(elements) - 1)
                    
                    elem_color = self.theme['primary'] if is_top else self.theme['accent']
                    
                    elem_frame = Frame(self.scrollable_frame, bg=elem_color, 
                                      relief=RAISED, bd=2)
                    elem_frame.pack(fill=X, padx=10, pady=3)
                    
                    label_text = f"TOP -> {value}" if is_top else str(value)
                    
                    Label(elem_frame, text=label_text, 
                          font=("Consolas", 11), fg='white',
                          bg=elem_color, anchor='w').pack(fill=X, padx=10, pady=5)
                            
        except Exception as e:
            Label(self.scrollable_frame, text=f"Ошибка: {e}", 
                  font=("Arial", 10), fg=self.theme['warning'],
                  bg=self.theme['bg']).pack(pady=20)
    
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def show_message(self, message, msg_type='info'):
        colors = {'success': self.theme['success'], 
                 'warning': self.theme['warning'], 
                 'info': self.theme['text_secondary']}
        
        self.status_label.config(text=message, fg=colors.get(msg_type, 'white'))
        self.root.after(3000, self.reset_status)
    
    def reset_status(self):
        self.status_label.config(text="Готов к работе", 
                                fg=self.theme['success'])


def main():
    root = Tk()
    app = ModernStackGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()