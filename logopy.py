import sys, traceback
from io import StringIO

from tkinter import *
from tkinter import scrolledtext


def make_ui():
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

  return editor_text, canvas, run_button, messages

editor_text, canvas, run_button, messages = make_ui()

class Logo:
  def __init__(self, canvas):
    self.canvas = canvas
    self.w = canvas.winfo_width()
    self.h = canvas.winfo_height()

    canvas.bind("<Configure>", self.canvas_resized)

    self.center = [self.w/2, self.h/2]
    self.point = [0, 0]

  def canvas_resized(self,e):
    self.w = self.canvas.winfo_width()
    self.h = self.canvas.winfo_height()
    self.center = [self.w/2, self.h/2]

    self.draw()

  def draw(self):
    self.canvas.delete("all")
    canvas.create_line(self.center[0], self.center[1], self.center[0] + self.point[0], self.center[1] + self.point[1])

  def forward(self, x, y):
    self.point = [x, y]


logo = Logo(canvas)

def run_func():
  code_string = editor_text.get(1.0, END)

  buffer = StringIO()
  sys.stdout = buffer
  sys.stderr = buffer

  try:
    eval(code_string)
  except Exception as ex:
    traceback.print_exc(file=sys.stdout)

  logo.draw()

  sys.stdout = sys.__stdout__
  sys.stderr = sys.__stderr__

  messages.delete(1.0, END)
  messages.insert(END, buffer.getvalue())

run_button["command"] = run_func
mainloop()
