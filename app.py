import tkinter as tk
from tkinter import ttk
from main import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Лемматизация текстов")
        self['background'] = '#EBEBEB'
        self.conf = {'padx': (5,15), 'pady':5}
        self.font = 'Helvetica 10'
        self.text = ''
        self.lemmatizator = ''
        self.put_frames()

    def put_frames(self):
        self.add_form_frame = AddForm(self).grid(row=0, column=0, sticky = 'nswe')
        self.add_result_frame = AddResult(self.master)

class AddForm(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self['font']=self.master.font

        self.put_widgets()
    
    def put_widgets(self):
        self.label_source = tk.Label(self, text="Исходный текст:", font=self.master.font)
        self.text_source = tk.Text(self, height=10, wrap="word", font=self.master.font)
        self.label_lemmatization = tk.Label(self, text="Выбор библиотеки для лемматизации:", font=self.master.font)
        self.combo_lemmatization = ttk.Combobox(self, width=20, font=self.master.font, values=["Pymorphy3", "Pymystem3"])
        self.btn_start = tk.Button(self, text="Выполнить лемматизацию", font=self.master.font, command=lambda: self.master.children['!addresult'].put_widgets())
        
        self.label_source.grid(row=0, column=0, sticky="w", cnf=self.master.conf)
        self.text_source.grid(row=1, column=0, columnspan=2, cnf=self.master.conf)
        self.label_lemmatization.grid(row=2, column=0, sticky="e", cnf=self.master.conf)
        self.combo_lemmatization.grid(row=2, column=1, cnf=self.master.conf)
        self.btn_start.grid(row=3, column=0, columnspan=2, cnf=self.master.conf)

    def grab_values(self):
        empty_string = ''
        length_empty_text = 1

        self.master.text = self.text_source.get("1.0", "end")
        self.master.lemmatizator = self.combo_lemmatization.get()
        
        # self.master.children['!addresult'].print_text()
        
        # if (lemmatizator == empty_string) and (length_empty_text == 1):
        #     self.text_source.delete("1.0", "end")
        #     self.text_source.insert("1.0", 'Выберите библиотеку')
        # elif (length_empty_text == 1):
        #     self.text_source.delete("1.0", "end")
        #     self.text_source.insert("1.0", 'Введите текст')


class AddResult(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.lemmatized_text = ''
        self.lead_time = 0

    def lemmatization(self):
        if text_validate(self.text) and self.lemmatizator != '':
            if self.lemmatizator == 'Pymorphy3':
                self.lemmatized_text, self.lead_time = pymorphy_lemmatization(self.text)
            elif self.lemmatizator == 'Pymystem3':
                self.lemmatized_text, self.lead_time = mystem_lemmatization(self.text)
    
    def put_values(self):
        self.master.children['!addform'].grab_values()
        self.text = self.master.text
        self.lemmatizator = self.master.lemmatizator
        self.lemmatization()

    def refresh(self):
        all_frames = [f for f in self.children]
        for widget in all_frames:
            self.nametowidget(widget).destroy()


    def put_widgets(self):
        self.put_values()
        self.refresh()

        self.label_output = tk.Label(self, text="Результат лемматизации:", font=self.master.font)
        self.text_output = tk.Text(self, height=10, wrap="word", font=self.master.font)
        self.text_output.insert("1.0", f'{self.lemmatized_text}')
        self.label_lead = tk.Label(self, text=f"Время работы библиотеки (мс): {self.lead_time*1000:.3f}", font=self.master.font)

        self.master.add_result_frame.grid(row=1, column=0, sticky = 'nswe')
        self.label_output.grid(row=4, column=0, columnspan=2, cnf=self.master.conf)
        self.text_output.grid(row=5, column=0, columnspan=2, cnf=self.master.conf)
        self.label_lead.grid(row=6, column=0, columnspan=2, cnf=self.master.conf)



if __name__ == '__main__':
    app = App()
    app.mainloop()