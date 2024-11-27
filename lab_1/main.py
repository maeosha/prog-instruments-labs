#!/usr/bin/env python3

import tkinter as t
import os, sys, i18n, webbrowser, subprocess, json
from Tape import Tape
from execute_code import import_code, execute_code, move, write, clear_tape
from generate_template import generate_template
from initialisation import initialisation


class U():
    def __init__(self):
        initialisation(self)

        w = 800
        h = 380
        r = t.Tk()
        r.geometry('%dx%d+%d+%d' % (w, h, int(r.winfo_screenwidth() / 2 - w / 2),
                                    int(r.winfo_screenheight() / 2 - h / 2)))
        r.resizable(width=False, height=False)
        r.title(i18n.t("main_title"))
        r.bind("<Control-o>", lambda y: import_code(self))

        self.i = {}
        self.e = ()
        self.c = {'14': [40, 20, self.color_blank], '13': [42, 40, self.color_blank], '12': [45, 60, self.color_blank],
                  '11': [49, 80, self.color_blank], '10': [54, 100, self.color_blank],
                  '9': [60, 120, self.color_blank], '8': [68, 140, self.color_blank], '7': [78, 160, self.color_blank],
                  '6': [90, 180, self.color_blank], '5': [104, 200, self.color_blank],
                  '4': [118, 220, self.color_blank], '3': [136, 237, self.color_blank],
                  '2': [156, 252, self.color_blank], '1': [178, 265, self.color_blank],
                  '0': [204, 270, self.color_blank],
                  '-1': [228, 265, self.color_blank], '-2': [250, 252, self.color_blank],
                  '-3': [270, 237, self.color_blank], '-4': [288, 220, self.color_blank],
                  '-5': [304, 200, self.color_blank],
                  '-6': [318, 180, self.color_blank], '-7': [330, 160, self.color_blank],
                  '-8': [340, 140, self.color_blank], '-9': [348, 120, self.color_blank],
                  '-10': [354, 100, self.color_blank],
                  '-11': [359, 80, self.color_blank], '-12': [363, 60, self.color_blank],
                  '-13': [366, 40, self.color_blank], '-14': [368, 20, self.color_blank]}
        tm = Tape()
        dp = os.getcwd()
        tp = os.getcwd() + "/default_templates"

        m = t.Menu(r)
        mf = t.Menu(tearoff=0)
        m.add_cascade(label=i18n.t("file"), menu=mf)
        mf.add_command(label=i18n.t("open"), command=lambda: import_code(self))
        mf.add_command(label=i18n.t("config_editor"), command=self.ce)
        mf.add_command(label=i18n.t("exit"), command=r.destroy)

        mt = t.Menu(tearoff=0)
        m.add_cascade(label=i18n.t("templates"), menu=mt)
        mt.add_command(label=i18n.t("generate"), command=lambda: generate_template(self))
        mlt = t.Menu(tearoff=0)
        mt.add_cascade(label=i18n.t("load"), menu=mlt)
        mlt.add_command(label=i18n.t("invert_value"), command=lambda: import_code(self, f"{tp}/invert_values.ptm"))
        mlt.add_command(label=i18n.t("add_one"), command=lambda: import_code(self, f"{tp}/add_one_binary.ptm"))
        mlt.add_command(label=i18n.t("remove_one"), command=lambda: import_code(self, f"{tp}/remove_one_binary.ptm"))

        ml = t.Menu(tearoff=0)
        m.add_cascade(label=i18n.t("language"), menu=ml)
        ml.add_command(label="English", command=lambda: self.cl("en"))
        ml.add_command(label="Français", command=lambda: self.cl("fr"))

        m.add_command(label=i18n.t("help"),
                      command=lambda: subprocess.Popen([os.getcwd() + "/documentation.pdf"], shell=True))

        m.add_command(label="Github", command=lambda: webbrowser.open("https://github.com/Yoween/PythonTuringMachine"))

        r.config(menu=m)

        self.et()
        self.pt()

    def et(self):
        try:
            self.rt.destroy()
        except:
            pass
        self.rt = t.Frame(self.root, bg='AntiqueWhite2')

        c2 = t.Canvas(self.rt, height=310, bg='AntiqueWhite2')
        c2.grid(row=1, column=0, columnspan=8, sticky='nesw')
        for v in self.c.values():
            self.dc(c2, v[0], v[1], 6, v[2])

        bg = t.Button(self.rt, text=i18n.t("start"), command=lambda: execute_code(self, self, self.i, sv.get()))
        bg.grid(row=10, column=0, padx=10, sticky='nesw')
        bcl = t.Button(self.rt, text=i18n.t("clear"), command=lambda: clear_tape(self, self))
        bcl.grid(row=10, column=1, sticky='nesw')
        bl = t.Button(self.rt, text=i18n.t("left"), command=lambda: move(self, self, "<"))
        bl.grid(row=10, column=2, sticky='nesw')
        br = t.Button(self.rt, text=i18n.t("right"), command=lambda: move(self, self, ">"))
        br.grid(row=10, column=3, sticky='nesw')
        cl = t.Label(self.rt, text=i18n.t("value"))
        cl.grid(row=10, column=4, padx=(10, 0), sticky='nesw')
        nl = t.Label(self.rt, text=i18n.t("next_value"))
        nl.grid(row=10, column=5, padx=(0, 10), sticky='nesw')

        sv = t.IntVar()
        bsl = t.Checkbutton(self.rt, text=i18n.t("slow"), variable=sv, offvalue=0, onvalue=1)
        bsl.grid(row=11, column=0, padx=10, sticky='nesw')
        bb = t.Button(self.rt, text="b", bg=self.color_blank, command=lambda: write(self, self, "b"))
        bb.grid(row=11, column=1, sticky='nesw')
        b0 = t.Button(self.rt, text="0", bg=self.color_zero, command=lambda: write(self, self, "0"))
        b0.grid(row=11, column=2, sticky='nesw')
        b1 = t.Button(self.rt, text="1", bg=self.color_one, command=lambda: write(self, self, "1"))
        b1.grid(row=11, column=3, sticky='nesw')
        cv = t.Label(self.rt, text="")
        cv.grid(row=11, column=4, padx=(10, 0), sticky='nesw')
        nv = t.Label(self.rt, text="")
        nv.grid(row=11, column=5, padx=(0, 10), sticky='nesw')

        self.rt.pack(side='right', expand=True, fill='both')
        for i in range(5):
            self.rt.columnconfigure(i, weight=1)

    def pt(self):
        try:
            self.lt.destroy()
        except:
            pass
        self.lt = t.Frame(self.root)

        self.sb(self.lt, self.root.winfo_screenwidth())

        tn = ("state", "read", "write", "move", "new_state")
        for i in range(5):
            self.__dict__[f"l_{tn[i]}"] = t.Label(self.sf, text=f"{i18n.t(tn[i])}", relief=t.RIDGE)
            self.__dict__[f"l_{tn[i]}"].grid(row=0, column=i, sticky='nesw')

        self.lt.pack(side='left', expand=True, fill='both')
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        for i in range(5):
            self.sf.columnconfigure(i, weight=1)

        x = 1
        while f"l_state{x}" in self.__dict__.keys():
            del self.__dict__[f"l_state{x}"]
            del self.__dict__[f"l_read{x}_b"]
            del self.__dict__[f"l_read{x}_0"]
            del self.__dict__[f"l_read{x}_1"]
            del self.__dict__[f"l_write{x}_b"]
            del self.__dict__[f"l_write{x}_0"]
            del self.__dict__[f"l_write{x}_1"]
            del self.__dict__[f"l_move{x}_b"]
            del self.__dict__[f"l_move{x}_0"]
            del self.__dict__[f"l_move{x}_1"]
            del self.__dict__[f"l_new_state{x}_b"]
            del self.__dict__[f"l_new_state{x}_0"]
            del self.__dict__[f"l_new_state{x}_1"]
            x += 1
        self.sf.update()

    def ns(self, ins):
        a = 1
        x = 1
        k = ("b", "0", "1")
        while a > 0:
            if not f'l_state{x}' in self.__dict__.keys():
                for i in range(3):
                    self.__dict__[f"l_state{x}"] = t.Label(self.sf, text=f"{x}")
                    self.__dict__[f"l_state{x}"].grid(row=3 * x - 1, column=0, sticky='nesw')
                    t.Label(self.sf, text='||').grid(row=3 * x, column=0, sticky='nesw')
                    t.Label(self.sf, text='||').grid(row=3 * x - 2, column=0, sticky='nesw')

                    self.__dict__[f"l_read{x}_{k[i]}"] = t.Label(self.sf, text=f"{k[i]}")
                    self.__dict__[f"l_read{x}_{k[i]}"].grid(row=3 * x - 2 + i, column=1, sticky='nesw')

                    self.__dict__[f"l_write{x}_{k[i]}"] = t.Label(self.sf, text=f"{ins[k[i]][0]}")
                    self.__dict__[f"l_write{x}_{k[i]}"].grid(row=3 * x - 2 + i, column=2, sticky='nesw')

                    self.__dict__[f"l_move{x}_{k[i]}"] = t.Label(self.sf, text=f"{ins[k[i]][1]}")
                    self.__dict__[f"l_move{x}_{k[i]}"].grid(row=3 * x - 2 + i, column=3, sticky='nesw')

                    self.__dict__[f"l_new_state{x}_{k[i]}"] = t.Label(self.sf, text=f'{ins[k[i]][2]}')
                    self.__dict__[f"l_new_state{x}_{k[i]}"].grid(row=3 * x - 2 + i, column=4, sticky='nesw')

                a -= 1
            x += 1

    def dc(self, c, x, y, r, cl):
        c.create_oval(x - r, y - r, x + r, y + r, width=0, fill=f'{cl}')

    def sb(self, c, w):
        self.canvas = t.Canvas(c, width=int(w / 7), bg='gray94')
        self.scrollbar = t.Scrollbar(c, orient="vertical", command=self.canvas.yview)
        self.sf = t.Frame(self.canvas)

        self.sf.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.sf, anchor="nw", width=int(w / 6))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def cl(self, l):
        with open(self.config_file, "w") as f:
            self.config["language"] = l
            json.dump(self.config, f)
        self.r()

    def cc(self, ch, cb, cz, co):
        for arg in vars().values():
            if arg == "":
                return
        with open(self.config_file, "w") as f:
            self.config["color_highlight"] = ch
            self.config["color_blank"] = cb
            self.config["color_zero"] = cz
            self.config["color_one"] = co
            json.dump(self.config, f)
        self.r()

    def ce(self):
        cw = t.Toplevel(self.root)
        cw.attributes('-topmost', 'true')
        self.root.eval(f'tk::PlaceWindow {str(cw)} center')
        t.Label(cw, text=i18n.t("config_editor")).pack()
        t.Label(cw, text=i18n.t("color_highlight")).pack()
        ch = t.Entry(cw)
        ch.pack()
        ch.insert(0, self.color_highlight)
        t.Label(cw, text=i18n.t("color_blank")).pack()
        cb = t.Entry(cw)
        cb.pack()
        cb.insert(0, self.color_blank)
        t.Label(cw, text=i18n.t("color_zero")).pack()
        cz = t.Entry(cw)
        cz.pack()
        cz.insert(0, self.color_zero)
        t.Label(cw, text=i18n.t("color_one")).pack()
        co = t.Entry(cw)
        co.pack()
        co.insert(0, self.color_one)
        t.Button(cw, text=i18n.t("save"), command=lambda: self.cc(ch.get(), cb.get(), cz.get(), co.get())).pack()
        t.Button(cw, text=i18n.t("cancel"), command=cw.destroy).pack()

    def r(self):
        rw = t.Toplevel(self.root)
        rw.attributes('-topmost', 'true')
        self.root.eval(f'tk::PlaceWindow {str(rw)} center')
        t.Label(rw, text=i18n.t("restart_required")).pack()
        t.Button(rw, text=i18n.t("indeed"), command=lambda: os.execv(sys.executable, ['python'] + sys.argv)).pack()
        t.Button(rw, text=i18n.t("please_no"), command=rw.destroy).pack()


if __name__ == '__main__':
    a = U()
    a.root.mainloop()


