import sys, traceback
from io import StringIO

from tkinter import *
from tkinter import scrolledtext




root_window = PanedWindow()
root_window.config(sashwidth=5, sashrelief=RAISED)
root_window.pack(fill=BOTH, expand=1)

editor_pane = PanedWindow(root_window, orient=VERTICAL)
editor_pane.config(sashwidth=5, sashrelief=RAISED)
root_window.add(editor_pane, width="400")

editor_and_run = Frame(editor_pane)
editor_pane.add(editor_and_run)

editor_text = scrolledtext.ScrolledText(editor_and_run)
editor_text.pack(fill=BOTH, expand=1)
run_button = Button(editor_and_run, text="Run")
run_button.pack()

messages = Text(editor_pane)
editor_pane.add(messages)

canvas = Canvas(root_window)
root_window.add(canvas, width="700")


def forward():
  canvas.create_line(0, 0, 10, 10)

def canvas_resized(event):
  print(canvas.winfo_width())
  print(canvas.winfo_height())

canvas.bind("<Configure>", canvas_resized)

def run_func():
  code_string = editor_text.get(1.0, END)

  buffer = StringIO()
  sys.stdout = buffer
  sys.stderr = buffer

  try:
    eval(code_string)
  except Exception as ex:
    traceback.print_exc(file=sys.stdout)

  sys.stdout = sys.__stdout__
  sys.stderr = sys.__stderr__

  messages.delete(1.0, END)
  messages.insert(END, buffer.getvalue())

run_button["command"] = run_func
mainloop()
