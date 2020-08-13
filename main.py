import algorithm
import tkinter as tk
import matplotlib.pyplot as plot
from random import randint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Test Case
# Seq: 98, 183, 37, 122, 14, 124, 65, 67
# Head: 53
# Prev: 70
# Cylinder: 199
def resetErrors():
    seqErrorLbl.config(fg='grey', bg='white')
    seqError.set('Separate with commas.')
    currError.set('')
    prevError.set('')
    cylinderError.set('')
    currRandError.set('')
    prevRandError.set('')
    cylindRandError.set('')


def start():
    orderVal.set('None')
    formulaVal.set('None')
    distanceVal.set('None')

    errorKeys = ('seq', 'curr', 'prev', 'cylinder')
    errors = {}

    seq = None
    cylinder = None
    head = None
    prev = None

    resetErrors()

    # Field validations
    if seqVal.get() == '':
        errors['seq'] = 'Sequences field is required!'
    elif seqVal.get().find(',') == -1:
        errors['seq'] = 'Sequence field requires integers separated with commas.'
    else:
        try:
            seq = [int(i) for i in seqVal.get().strip().split(',')]
        except:
            errors['seq'] = 'Sequence field requires multiple integer separated with commas.'

    if currVal.get() == '':
        errors['curr'] = 'Current field is required!'
    else:
        try:
            head = int(currVal.get())
        except ValueError:
            errors['curr'] = 'Current field to be an integer.'

    if prevVal.get() == '':
        errors['prev'] = 'Previous field is required!'
    else:
        try:
            prev = int(prevVal.get())
        except ValueError:
            errors['prev'] = 'Previous field has to be an integer.'

    if cylinderVal.get() == '':
        errors['cylinder'] = 'Cylinder field is required!'
    else:
        try:
            cylinder = int(cylinderVal.get())
        except ValueError:
            errors['cylinder'] = 'Cylinder field has to be an integer.'

    # If any errors, display error message
    if any([x in errorKeys for x in errors]):
        if 'seq' in errors:
            seqErrorLbl.config(fg='red')
            seqError.set(errors['seq'])
        if 'curr' in errors:
            currError.set(errors['curr'])
        if 'prev' in errors:
            prevError.set(errors['prev'])
        if 'cylinder' in errors:
            cylinderError.set(errors['cylinder'])

        ax.clear()
        plot.title('Sequences')
        canvas.draw()
    else:   # else attempt to start selected algorithm
        resetErrors()

        alg = algorithm.Algorithm(seq, cylinder, head, prev)
        results = alg.start(algVal.get())

        if results:
            orderVal.set(', '.join(str(v) for v in results['sequence']))
            formulaVal.set(results['formula'])
            distanceVal.set(results['distance'])

            # Plot graph
            y = results['sequence']
            x = [i for i in range(len(results['sequence']))]

            ax.clear()
            plot.tight_layout()
            plot.title('Sequences')
            ax.plot(x, y, color='#78909C', marker='o', markerfacecolor='#00BCD4', markersize=10)

            # Assign plot label
            for i in range(len(results['sequence'])):
                ax.text(x[i] + 0.1, y[i] - 0.15, str(y[i]))

            canvas.draw()


def randSeq():
    resetErrors()
    seq = [randint(1, 9998) for i in range(randint(6, 15))]
    seqVal.set(str(seq)[1: -2].strip())


def randCurr():
    resetErrors()

    error = None

    if seqVal.get() == '':
        error = 'Sequences field is required first.'
    elif seqVal.get().find(',') == -1:
        error = 'Sequence field requires integers separated with commas first.'
    else:
        try:
            [int(i) for i in seqVal.get().strip().split(',')]
        except:
            error = 'Sequence field requires multiple integer separated with commas first.'

    if error is not None:
        currRandError.set(error)
    else:
        seq = [int(v) for v in seqVal.get().split(',')]
        curr = 0

        while curr == 0:
            curr = randint(1, 9998)

            if curr in seq:
                curr = 0

        currVal.set(curr)


def randPrev():
    resetErrors()

    error = None

    if seqVal.get() == '':
        error = 'Sequences field is required first.'
    elif seqVal.get().find(',') == -1:
        error = 'Sequence field requires integers separated with commas first.'
    else:
        try:
            [int(i) for i in seqVal.get().strip().split(',')]
        except:
            error = 'Sequence field requires multiple integer separated with commas first.'

    if error is not None:
        prevRandError.set(error)
    else:
        seq = [int(v) for v in seqVal.get().split(',')]
        prev = 0

        while prev == 0:
            prev = randint(1, 9998)

            if prev in seq:
                prev = 0

        prevVal.set(prev)


def randCylinder():
    resetErrors()

    error = None

    if seqVal.get() == '':
        error = 'Sequences field is required first.'
    elif seqVal.get().find(',') == -1:
        error = 'Sequence field requires integers separated with commas first.'
    else:
        try:
            [int(i) for i in seqVal.get().strip().split(',')]
        except:
            error = 'Sequence field requires multiple integer separated with commas first.'

    if error is not None:
        cylindRandError.set(error)
    else:
        seq = [int(v) for v in seqVal.get().split(',')]
        cylinder = 0

        while cylinder == 0:
            cylinder = randint(max(seq) + 1, 9998)

            if cylinder in seq:
                cylinder = 0

        cylinderVal.set(cylinder)


def randAll():
    randSeq()
    randCurr()
    randPrev()
    randCylinder()


if __name__ == '__main__':
    # Main Window
    win = tk.Tk()
    win.title('Disk Optimization')
    win.iconbitmap('icon.ico')
    win.configure(bg='white')

    # Default Elements Styles

    # Algorithm Elements
    algorithms = {
        'FCFS': 'fcfs',
        'SSTF': 'sstf',
        'SCAN': 'scan',
        'LOOK': 'look',
        'C-SCAN': 'cscan',
        'C-LOOK': 'clook'
    }

    algVal = tk.StringVar()
    algVal.set('fcfs')

    tk.Label(win, text='Algorithm: ', bg='white', justify='left').grid(row=0, padx=10, sticky='w')

    i = 1
    for k, v in algorithms.items():
        tk.Radiobutton(win, text=k, value=v, variable=algVal, bg='white').grid(row=0, column=i, padx=10, sticky='we')
        i += 1

    # Random All Button Element
    tk.Button(win, text='Generate Random All', fg='white', bg='#607D8B', highlightbackground='#607D8B', relief='flat', command=randAll).grid(row=0, column=i, pady=5, padx=10, sticky='we')

    # Sequences Elements
    seqVal = tk.StringVar()

    tk.Label(win, text='Sequences:', justify='left', bg='white').grid(row=1, padx=10, sticky='w')
    tk.Entry(win, textvariable=seqVal).grid(row=1, column=1, columnspan=6, sticky='we')
    tk.Button(win, text='Generate Random Sequences', fg='white', bg='#00BCD4', highlightbackground='#00BCD4', relief='flat', command=randSeq).grid(row=1, column=7, padx=10, sticky='we')

    # Sequences Entry Error
    seqError = tk.StringVar()
    seqError.set('Separate with commas.')

    seqErrorLbl = tk.Label(win, text='Separate with comma', textvariable=seqError, fg='grey', bg='white', font='TkDefaultFont, 7', justify='left')
    seqErrorLbl.grid(row=2, column=1, columnspan=7, sticky='w')

    # Current Elements
    currVal = tk.StringVar()
    currError = tk.StringVar()

    tk.Label(win, text='Current:', bg='white', justify='left').grid(row=3, padx=10, sticky='w')
    tk.Entry(win, textvariable=currVal).grid(row=3, column=1, columnspan=6, sticky='we')
    tk.Button(win, text='Generate Random Current', fg='white', bg='#00BCD4', highlightbackground='#00BCD4', relief='flat', command=randCurr).grid(row=3, column=7, padx=10, sticky='we')

    # Current Entry Error Text
    tk.Label(win, textvariable=currError, fg='red', bg='white', font='TkDefaultFont, 7', justify='left').grid(row=4, column=1, columnspan=6, sticky='w')

    # Current Random Error
    currRandError = tk.StringVar()

    tk.Label(win, textvariable=currRandError, fg='red', bg='white', font='TkDefaultFont, 7', justify='left').grid(row=4, column=7, padx=10, sticky='w')

    # Previous Elements
    prevVal = tk.StringVar()
    prevError = tk.StringVar()

    tk.Label(win, text='Previous:', bg='white', justify='left').grid(row=5, padx=10, sticky='w')
    tk.Entry(win, textvariable=prevVal).grid(row=5, column=1, columnspan=6, sticky='we')
    tk.Button(win, text='Generate Random Previous', fg='white', bg='#00BCD4', highlightbackground='#00BCD4', relief='flat', command=randPrev).grid(row=5, column=7, padx=10, sticky='we')

    # Previous Entry Error
    tk.Label(win, text='', textvariable=prevError, fg='red', bg='white', font='TkDefaultFont, 7', justify='left').grid(row=6, column=1, columnspan=6, sticky='w')

    # Previous Random Error
    prevRandError = tk.StringVar()

    tk.Label(win, textvariable=prevRandError, fg='red', bg='white', font='TkDefaultFont, 7', justify='left').grid(row=6, column=7, padx=10, sticky='w')

    # Cylinder Elements
    cylinderVal = tk.StringVar()
    cylinderError = tk.StringVar()

    tk.Label(win, text='Cylinder:', bg='white', justify='left').grid(row=7, padx=10, sticky='w')
    tk.Entry(win, textvariable=cylinderVal).grid(row=7, column=1, columnspan=6, sticky='we')
    tk.Button(win, text='Generate Random Cylinder', fg='white', bg='#00BCD4', highlightbackground='#00BCD4', relief='flat', command=randCylinder).grid(row=7, column=7, padx=10, sticky='we')

    # Cylinder Entry Error
    tk.Label(win, text='', textvariable=cylinderError, fg='red', bg='white', font='TkDefaultFont, 7', justify='left').grid(row=8, column=1, columnspan=6, sticky='w')

    # Cylinder Random Error
    cylindRandError = tk.StringVar()

    tk.Label(win, textvariable=cylindRandError, fg='red', bg='white', font='TkDefaultFont, 7', justify='left').grid(row=8, column=7, padx=10, sticky='w')

    # Start Button Element
    tk.Button(win, text='Start', font='TkDefaultFont, 10', fg='white', bg='#009688', highlightbackground='#009688', relief='flat', command=start).grid(row=9, columnspan=8, pady=5, padx=250, sticky='we')

    # Spacing
    tk.Label(win, bg='white').grid(row=10, columnspan=8)

    # Results Elements
    tk.Label(win, text='RESULTS', font='TKDefaultFont, 14', bg='white', borderwidth=1, relief='solid').grid(row=11, columnspan=8, pady=15, padx=10, sticky='we')

    # Graph Elements
    fig, ax = plot.subplots(facecolor='#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    plot.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=win)
    plotCanvas = canvas.get_tk_widget()

    plot.title('Sequences')
    plotCanvas.grid(row=12, columnspan=8, pady=10, padx=10, sticky='we')

    # Order Elements
    orderVal = tk.StringVar()
    orderVal.set('None')

    tk.Label(win, text='Order: ', bg='white').grid(row=13, pady=2, padx=10, sticky='w')
    tk.Label(win, textvariable=orderVal, bg='white', justify='left', anchor='w').grid(row=13, column=1, columnspan=6, padx=10, sticky='we')

    # Formula Elements
    formulaVal = tk.StringVar()
    formulaVal.set('None')

    tk.Label(win, text='Formula: ', bg='white').grid(row=14, pady=2, padx=10, sticky='w')
    tk.Label(win, textvariable=formulaVal, bg='white', justify='left', anchor='w').grid(row=14, column=1, columnspan=6, pady=2, padx=10, sticky='we')

    # Distance Elements
    distanceVal = tk.StringVar()
    distanceVal.set('None')

    tk.Label(win, text='Distance: ', bg='white').grid(row=15, pady=2, padx=10, sticky='w')
    tk.Label(win, textvariable=distanceVal, bg='white', justify='left', anchor='w').grid(row=15, column=1, columnspan=6, pady=2, padx=10, sticky='we')

    # Spacing
    tk.Label(win, font='TKDefaultFont, 5', bg='white').grid(row=16, columnspan=8)

    win.mainloop()
