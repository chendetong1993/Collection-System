from tkinter import *
import uuid
import os
import json
import tkinter.filedialog

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      self.picks = picks;
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      res = []
      for idx, var in enumerate(self.vars):
          if(var.get() > 0):
              res.append(self.picks[idx])
      return res

class Radiobar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.var = IntVar()
      self.picks = picks;
      for idx, pick in enumerate(picks):
         chk = Radiobutton(self, text=pick, variable=self.var, value = idx)
         chk.pack(side=side, anchor=anchor, expand=YES)
   def state(self):
      return self.picks[self.var.get()]

if __name__ == '__main__':

   # configuration
   envir_groups = ['1900', '2000', '2200', '2400']
   tag_groups = ['Head','Foot']
   dst_dir = "./"

   root = Tk()
   envir = Radiobar(root, envir_groups)
   tag = Checkbar(root, tag_groups)
   envir.pack(side=TOP,  fill=X)
   tag.pack(side=LEFT)
   envir.config(relief=GROOVE, bd=2)

   def allstates():
      src_paths = tkinter.filedialog.askopenfilenames(filetypes=[("oni file", "*.oni"),("all","*.*")])
      for src_path in src_paths:
          dst_filename = envir.state() + "_" +  '_'.join(tag.state()) + "_" + ''.join(str(uuid.uuid1()).split('-'))
          dst_path = dst_dir + dst_filename + os.path.splitext(src_path)[1]
          print("Move " + src_path + " to " + dst_path)
          os.rename(src_path, dst_path)
 
          with open(dst_dir + dst_filename + ".ini",'w') as f:
              json.dump({ "envir": envir.state(), "tags": tag.state()}, f)


   Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
   Button(root, text='Tag', command=allstates).pack(side=RIGHT)
   
   
   root.mainloop()