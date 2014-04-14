from tkinter import *
from ttk import * # sudo pip3 install pyttk

import gui
from gui import new, bundle, top, root
import ssa.final as core

fmv = dict()
fmf = dict()
fmw = dict()

#/Users/sean/github/vermiculus/smp/ssa-tool/exam/ind-set.ssax
def load_bundle():
    path = fmv['bundle path'].get()
    msg = 'Loading bundle {}...'.format(path[path.rfind('/')+1:])
    print(msg)
    bundle.load(path)
    print(msg + ' Done.')
    fmf['bundle to gui']()


def refresh():
    """Clears all front-facing data and reloads it from the code-behind"""
    from gui import agw, pdw, mvw, agv, pdv, mvv, agf

    # clear the widgets
    for wd in [agw, pdw, mvw]:
        for w in wd:
            if isinstance(wd[w][1], Listbox):
                wd[w][1].delete(0, END)
    for v in [agv, pdv, mvv]:
        if isinstance(v, StringVar):
            v.set('')

    # populate the widgets
    for alg in bundle.types(core.Algorithm):
        agw['algorithm list'][1].insert(END, alg.name)
    for move in bundle.types(core.Move):
        mvw['list'][1].insert(END, move.name)
    for pred in bundle.types(core.Predicate):
        pdw['list'][1].insert(END, pred.name)

def bdl2dsk():
    path = fmv['bundle path'].get()
    msg = 'Saving bundle {}...'.format(path[path.rfind('/')+1:])
    print(msg)
    from gui import agf, pdf, mvf
    for f in [agf, pdf, mvf]:
        if 'finalize' in f:
            f['finalize']()
    bundle.dump(path)
    print(msg + ' Done.')

fmf['bundle to gui'] = refresh
fmf['save bundle'] = bdl2dsk
fmf['load bundle'] = load_bundle

fmv['bundle path'] = StringVar(root)

fmw['tab']                = None , Frame(top)
fmw['title']              = (210,  20) , new(Label  , fmw , 'tab' , text = 'SSA TOOL', font=('Helvetica', 24))
#fmw['new bundle']         = (220,  60) , new(Button , fmw , 'tab' , text = 'new bundle')
fmw['bundle path']        = (190, 170) , new(Entry  , fmw , 'tab' , textvariable = fmv['bundle path'])
fmw['save bundle']        = (220, 200) , new(Button , fmw , 'tab' , text = 'save bundle' , command = fmf['save bundle'])
fmw['load bundle']        = (220, 235) , new(Button , fmw , 'tab' , text = 'load bundle' , command = fmf['load bundle'])

# Local Variables:
# truncate-lines: t
# End:
