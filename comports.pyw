import serial.tools.list_ports
import usb_ids
import tkinter.ttk
import subprocess


def main():
    comports = serial.tools.list_ports.comports()

    top = tkinter.Tk()
    top.title('COM Ports')

    ports_listbox = tkinter.Listbox(top, width=150, height=15, exportselection=False)
    ports_listbox.pack(fill=tkinter.BOTH, expand=1)
    
    for i in comports:
        ports_listbox.insert(tkinter.END, '%s: %s [%s %s]' % (i.device, i.description, *usb_ids.get(i.vid or 0, i.pid or 0)))

    ports_listbox.select_set(0, 0)

    baud_rate_combobox = tkinter.ttk.Combobox(top)
    baud_rate_combobox.pack(side=tkinter.LEFT)
    
    baud_rate_combobox['values'] = list(map(str, (110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000)))
    baud_rate_combobox.set('115200')

    ports_listbox.focus()

    def ok(event=None):
        sel = ports_listbox.curselection()
        print(sel)
        if sel:
            com_port = comports[sel[0]].device
            baud_rate = baud_rate_combobox.get()
            cmd = ['putty', '-serial', com_port, '-sercfg', baud_rate + ',8,n,1,N']

            print(' '.join(cmd))
            subprocess.Popen(cmd)

        top.destroy()

    def cancel(event=None):
        top.destroy()

    top.bind('<Return>', ok)
    top.bind('<Escape>', cancel)

    top.focus_force()
    top.mainloop()


if __name__ == '__main__':
    main()
