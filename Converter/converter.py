import csv

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class Converter:
    def __init__(self) -> None:
        self.app = tk.Tk()

        self.frame1 = ttk.Frame(master=self.app)
        self.frame2 = ttk.Frame(master=self.app)

        self.frame1.grid(column=0, row=0)
        self.frame2.grid(column=0, row=1)

        self.open_button = ttk.Button(master=self.frame1, text='Open', command=self.open_file)
        self.open_button.grid(column=0, row=0)

        self.convert_button = ttk.Button(master=self.frame1, text='Convert', command=self.convert_file)
        self.convert_button.grid(column=1, row=0)
        self.convert_button.config(state=tk.DISABLED)

        self.progress_bar = ttk.Progressbar(master=self.frame2, mode='determinate')
        self.progress_bar.grid(column=0, row=0)

        self.app.mainloop()

    def open_file(self) -> None:
        self.open_button.config(state=tk.DISABLED)

        self.filename = filedialog.askopenfilename(defaultextension='csv', initialdir='database')

        if self.filename != '':
            self.convert_button.config(state=tk.NORMAL)

        self.open_button.config(state=tk.NORMAL)

    def convert_file(self) -> None:
        self.open_button.config(state=tk.DISABLED)
        self.convert_button.config(state=tk.DISABLED)

        output_filename = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension='csv', initialdir='database')

        with open(self.filename, 'r', encoding='utf8') as input_file:
            with open(output_filename, 'w', encoding='utf8') as output_file:
                line_count = len(input_file.readlines()) - 1
                print(line_count)

                input_file.seek(0)

                reader = csv.DictReader(input_file)

                if reader.fieldnames is not None:
                    fieldnames = reader.fieldnames
                else:
                    fieldnames = []

                writer = csv.DictWriter(output_file, fieldnames=fieldnames)

                writer.writeheader()

                output_list: list[dict[str, str]] = []

                for line_number, row in enumerate(reader):
                    output_list.append(row)
                    if (line_number % 10000) == 0:
                        writer.writerows(output_list)
                        output_list.clear()
                        print(line_number)
                        self.progress_bar['value'] = int((line_number / line_count) * 100)
                        self.progress_bar.update()

                writer.writerows(output_list)
                output_list.clear()

        self.convert_button.config(state=tk.NORMAL)
        self.open_button.config(state=tk.NORMAL)
