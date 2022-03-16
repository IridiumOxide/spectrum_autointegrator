import tkinter as tk
import tkinter.filedialog
import sys

import integration


class IntegrationConfig():
    def __init__(self, file, start, end, separator, euro, nobase):
        self.file = file
        self.start = start
        self.end = end
        self.separator = separator
        self.euro = euro
        self.nobase = nobase


def main(argv):
    create_gui()


def browse_directory(filepath_entry):
    def browse_file_func():
        dir_name = tk.filedialog.askdirectory(mustexist=True)
        filepath_entry.insert(tk.END, dir_name)
    return browse_file_func


def create_gui():
    window = tk.Tk()

    # TODO: choose directory or file mode
    filepath_widget = tk.Frame(window)
    filepath_entry = tk.Entry(filepath_widget, width=50)
    filepath_entry.pack(anchor="w")
    filepath_button = tk.Button(filepath_widget, text="Choose directory", command=browse_directory(filepath_entry))
    filepath_button.pack(anchor="w")

    integration_details_widget = tk.Frame(window)
    integration_range_start_entry = tk.Entry(integration_details_widget)
    integration_range_start_entry.insert(tk.END, str(600.0))
    integration_range_start_entry.pack(anchor="w")
    integration_range_end_entry = tk.Entry(integration_details_widget)
    integration_range_end_entry.insert(tk.END, str(1000.0))
    integration_range_end_entry.pack(anchor="w")

    csv_separator_var = tk.StringVar(None, ";")
    csv_separator_widget = tk.Frame(window)
    csv_separator_entry_label = tk.Label(csv_separator_widget, text="CSV value separator")
    csv_separator_entry_label.pack(anchor="w")
    csv_separator_entry_comma = tk.Radiobutton(csv_separator_widget, text="Comma separated (ex. A,1,2.34)", variable=csv_separator_var, value=",")
    csv_separator_entry_comma.pack(anchor="w")
    csv_separator_entry_semicolon = tk.Radiobutton(csv_separator_widget, text="Semicolon separated (ex. A;1;2.34)", variable=csv_separator_var, value=";")
    csv_separator_entry_semicolon.pack(anchor="w")
    csv_separator_entry_pipe = tk.Radiobutton(csv_separator_widget, text="Pipe separated  (ex. A|1|2.34)", variable=csv_separator_var, value="|")
    csv_separator_entry_pipe.pack(anchor="w")
    csv_separator_entry_space = tk.Radiobutton(csv_separator_widget, text="Space separated (ex. A 1 2.34)", variable=csv_separator_var, value=" ")
    csv_separator_entry_space.pack(anchor="w")

    euro_var = tk.BooleanVar(None, False)
    euro_widget = tk.Frame(window)
    euro_entry_label = tk.Label(euro_widget, text="Number decimal separator")
    euro_entry_label.pack(anchor="w")
    euro_entry_dot = tk.Radiobutton(euro_widget, text="Dot separated   (ex. 1.234)", variable=euro_var, value=False)
    euro_entry_dot.pack(anchor="w")
    euro_entry_comma = tk.Radiobutton(euro_widget, text="Comma separated (ex. 1,234)", variable=euro_var, value=True)
    euro_entry_comma.pack(anchor="w")

    filepath_widget.pack(anchor="w", padx=10, pady=10)
    csv_separator_widget.pack(anchor="w", padx=10, pady=10)
    euro_widget.pack(anchor="w", padx=10, pady=10)
    integration_details_widget.pack(anchor="w", padx=10, pady=10)

    run_integration_widget = tk.Frame(window)
    start = tk.Button(run_integration_widget, text="Integrate!", width=25, height=10,
                      command=run_integration(
                          IntegrationConfig(
                              filepath_entry.get(),
                              0,
                              1,
                              csv_separator_var.get(),
                              euro_var.get(),
                              False,
                          )
                      )
                      )
    start.pack(anchor="w", padx=10, pady=10)

    tk.mainloop()


def run_integration(filepath_entry, ):
    def r_i():
        print("test")
    return r_i


if __name__ == "__main__":
    main(sys.argv[1:])
