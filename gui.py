# http://stackoverflow.com/a/16532192/1443496
from tkinter import *
from ttk import * # sudo pip3 install pyttk

import ssa.final as core

import time

class Test:
    count = 0
    def __init__(self):
        self.name = 'test class with str'
        self.n = Test.count
        Test.count += 1
    def __str__(self):
        return '({!s}) {}'.format(self.n, time.asctime())

print ('Building interface...')

root = Tk()
root.title('SSA Graphical Aggregator')
root.geometry('600x400+5+5')
top = Notebook(root, width=1000, height=400)

# we only technically deal with one bundle at a time
bundle = core.Bundle()
# data binding between names and objects
bind                 = dict()
bind[core.Bundle]    = dict()
bind[core.Predicate] = dict()
bind[core.Move]      = dict()
bind[core.Rule]      = dict()
bind[core.Algorithm] = dict()

# variables / functions / widgets
fmv, fmf, fmw = dict(), dict(), dict() # file management
agv, agf, agw = dict(), dict(), dict() # algorithm
pdv, pdf, pdw = dict(), dict(), dict() # predicate
mvv, mvf, mvw = dict(), dict(), dict() # move

# by giving the widget dictionary and the name separately, we can
# defer the evaulation of the listbox control until such a time as it
# is actually created.
def add_new(widget_dictionary, name, cls=Test):
    """Adds a new item"""
    def f(entity = None):
        if not entity: entity = cls()
        entity.name = '<new>'
        bind[cls]
        widget_dictionary[name][1].insert(END, entity.name)
    return f
def del_sel(widget_dictionary, name):
    """Deletes the selected item"""
    def f():
        widget_dictionary[name][1].delete(ACTIVE)
    return f
def move(widget_dictionary, lb1, lb2):
    """Moves the ACTIVE item from lb1 to lb2

    lb1 and lb2 are names that are in the widget_dictionary
    """
    def f():
        active = widget_dictionary[lb1][1].get(ACTIVE)
        if str(active) != '':   # to avoid moving empty items
            widget_dictionary[lb1][1].delete(ACTIVE)
            widget_dictionary[lb2][1].insert(END, active)
    return f
def new(cls, widget_dictionary, name, **kwargs):
    print('Creating widget {0:<14} under {1}'.format(cls.__name__, name))
    return cls(widget_dictionary[name][1], **kwargs)

################################################################
### File Manager ###############################################
################################################################

#/Users/sean/github/vermiculus/smp/ssa-tool/examples/ind-set.ssax
def load_bundle():
    path = fmv['bundle path'].get()
    msg = 'Loading bundle {}...'.format(path[path.rfind('/')+1:])
    print(msg)
    bundle.load(path)
    print(msg + ' Done.')
    fmf['refresh']()
fmf['load bundle'] = load_bundle

def refresh():
    """Clears all front-facing data and reloads it from the code-behind"""

    # Clear the bindings
    print('refreshing')
    bind                 = dict()
    bind[core.Bundle]    = dict()
    bind[core.Predicate] = dict()
    bind[core.Move]      = dict()
    bind[core.Rule]      = dict()
    bind[core.Algorithm] = dict()

    # clear the widgets
    for wd in [agw, pdw, mvw]:
        for w in wd:
            if isinstance(wd[w][1], Listbox):
                wd[w][1].delete(0, END)

    # populate the widgets
    for alg in bundle.types(core.Algorithm):
        agw['algorithm list'][1].insert(END, alg.name)
    for move in bundle.types(core.Move):
        mvw['list'][1].insert(END, move.name)
    for pred in bundle.types(core.Predicate):
        pdw['list'][1].insert(END, pred.name)
    

fmf['refresh'] = refresh

fmv['bundle path'] = StringVar(root)

fmw['tab']                = None , Frame(top)
fmw['title']              = (210,  20) , new(Label  , fmw , 'tab' , text = 'SSA TOOL', font=('Helvetica', 24))
fmw['new bundle']         = (220,  60) , new(Button , fmw , 'tab' , text = 'new bundle')
fmw['bundle path']        = (190, 170) , new(Entry  , fmw , 'tab' , textvariable = fmv['bundle path'])
fmw['save bundle']        = (220, 200) , new(Button , fmw , 'tab' , text = 'save bundle')
fmw['load bundle']        = (220, 235) , new(Button , fmw , 'tab' , text = 'load bundle' , command = fmf['load bundle'])

################################################################
### Algorithms #################################################
################################################################

agv['predicate']          = StringVar(root)
agv['algorithm name']     = StringVar(root)
agv['algorithm author']   = StringVar(root)
agv['algorithm date']     = StringVar(root)
agv['rule name']          = StringVar(root)
agv['rule author']        = StringVar(root)
agv['rule date']          = StringVar(root)
agv['predicate options']  = [Test(), Test(), Test(), Test()]

agv['predicate'].set(agv['predicate options'][0])

agf['add algorithm']      = add_new(agw, 'algorithm list', core.Algorithm)
agf['delete algorithm']   = del_sel(agw, 'algorithm list')
agf['add rule']           = add_new(agw, 'rule list', core.Rule)
agf['delete rule']        = del_sel(agw, 'rule list')
agf['add move']           = move(agw, 'move list', 'move list for rule')
agf['delete move']        = move(agw, 'move list for rule', 'move list')

agw['tab']                =    None ,        Frame(top)
agw['rule group']         = (   165 ,   40), new(Labelframe, agw, 'tab', text = 'Rules', height=300, width=775)
agw['name']               = (   165 ,    0), new(Entry,   agw, 'tab',        textvariable = agv['algorithm name'])
agw['author']             = (   340 ,    0), new(Entry,   agw, 'tab',        textvariable = agv['algorithm author'])
agw['date']               = (   340 ,   25), new(Entry,   agw, 'tab',        textvariable = agv['algorithm date'])
agw['rule name']          = (   170 ,    0), new(Entry,   agw, 'rule group', textvariable = agv['rule name'])
agw['rule date']          = (   170 ,   25), new(Entry,   agw, 'rule group', textvariable = agv['rule date'])
agw['rule author']        = (   170 ,   50), new(Entry,   agw, 'rule group', textvariable = agv['rule author'])
agw['alg  add']           = (     0 ,  310), new(Button,  agw, 'tab',        text = 'add', command = agf['add algorithm'])
agw['alg  del']           = (    80 ,  310), new(Button,  agw, 'tab',        text = 'del', command = agf['delete algorithm'])
agw['rule add']           = (     0 ,  110), new(Button,  agw, 'rule group', text = 'add', command = agf['add rule'])
agw['rule del']           = (    80 ,  110), new(Button,  agw, 'rule group', text = 'del', command = agf['delete rule'])
agw['move add']           = (   140 ,  175), new(Button,  agw, 'rule group', text = '>', command = agf['add move'])
agw['move del']           = (   140 ,  200), new(Button,  agw, 'rule group', text = '<', command = agf['delete move'])
agw['algorithm list']     = (     0 ,    0), new(Listbox, agw, 'tab',        height = 18)
agw['rule list']          = (     0 ,    0), new(Listbox, agw, 'rule group', height = 6)
agw['move list']          = (     0 ,  140), new(Listbox, agw, 'rule group', height = 7)
agw['move list for rule'] = (   200 ,  140), new(Listbox, agw, 'rule group', height = 7)
agw['rule predicate']     = (   170 ,   75), OptionMenu(agw['rule group'][1], agv['predicate'], agv['predicate options'][0], *agv['predicate options'])

################################################################
### Predicates #################################################
################################################################

pdf['add']         = add_new(pdw, 'list', core.Predicate)
pdf['remove']      = del_sel(pdw, 'list')

pdv['name']        = StringVar(root)
pdv['file']        = StringVar(root)
pdv['author']      = StringVar(root)
pdv['date']        = StringVar(root)
pdv['description'] = StringVar(root)
pdv['tex']         = StringVar(root)

pdw['tab']         = None ,        Frame(top)
pdw['list']        = (0   ,   0) , new(Listbox, pdw, 'tab' , height = 18)
pdw['name']        = (180 ,   0) , new(Entry,   pdw, 'tab' , textvariable = pdv['name'])
pdw['author']      = (360 ,   0) , new(Entry,   pdw, 'tab' , textvariable = pdv['author'])
pdw['date']        = (180 ,  25) , new(Entry,   pdw, 'tab' , textvariable = pdv['date'])
pdw['file']        = (360 ,  50) , new(Entry,   pdw, 'tab' , textvariable = pdv['file'])
pdw['description'] = (180 ,  50) , new(Entry,   pdw, 'tab' , textvariable = pdv['description'])
pdw['tex']         = (360 ,  25) , new(Entry,   pdw, 'tab' , textvariable = pdv['tex'])
pdw['add']         = (0   , 310) , new(Button,  pdw, 'tab' , text = 'add'    , command = pdf['add'])
pdw['remove']      = (80  , 310) , new(Button,  pdw, 'tab' , text = 'remove' , command = pdf['remove'])
pdw['definition']  = (180 ,  80) , new(Text,    pdw, 'tab' , width = 49, height = 16)

################################################################
### Moves ######################################################
################################################################

mvf['add']         = add_new(mvw, 'list', core.Move)
mvf['remove']      = del_sel(mvw, 'list')

mvv['name']        = StringVar(root)
mvv['file']        = StringVar(root)
mvv['author']      = StringVar(root)
mvv['date']        = StringVar(root)
mvv['description'] = StringVar(root)
mvv['tex']         = StringVar(root)

mvw['tab']         = None ,        Frame(top)
mvw['list']        = (0   ,   0) , new(Listbox, mvw, 'tab' , height = 18)
mvw['name']        = (180 ,   0) , new(Entry,   mvw, 'tab' , textvariable = mvv['name'])
mvw['author']      = (360 ,   0) , new(Entry,   mvw, 'tab' , textvariable = mvv['author'])
mvw['date']        = (180 ,  25) , new(Entry,   mvw, 'tab' , textvariable = mvv['date'])
mvw['file']        = (360 ,  50) , new(Entry,   mvw, 'tab' , textvariable = mvv['file'])
mvw['description'] = (180 ,  50) , new(Entry,   mvw, 'tab' , textvariable = mvv['description'])
mvw['tex']         = (360 ,  25) , new(Entry,   mvw, 'tab' , textvariable = mvv['tex'])
mvw['add']         = (0   , 310) , new(Button,  mvw, 'tab' , text = 'add'    , command = mvf['add'])
mvw['remove']      = (80  , 310) , new(Button,  mvw, 'tab' , text = 'remove' , command = mvf['remove'])
mvw['definition']  = (180 ,  80) , new(Text,    mvw, 'tab' , width = 49, height = 16)

# DEBUG Widgets bear their names for sanity
for vd in [fmv, agv, pdv, mvv]:
    for v in vd:
        if isinstance(vd[v], StringVar):
            vd[v].set(v)
for wd in [fmw, agw, pdw, mvw]:
    for w in wd:
        if isinstance(wd[w][1], Listbox):
            wd[w][1].insert(END, w)

# Place all widgets according to the coordinates given as the first
# element of the tuple.  If the first element of the tuple evaluates
# to False (that is, bool(...) is False), then simply pack the widget.
for widgets in [fmw, agw, pdw, mvw]:
    for widget in widgets:
        if widgets[widget][0]:
            print('placing {0:<20}   at ({1:>4}, {2:>4})'.format(widget, *widgets[widget][0]))
            pos = widgets[widget][0]
            wgt = widgets[widget][1]
            wgt.place(x=pos[0], y=pos[1])
        else:
            if widget not in ['tab']:
                print('No coordinates for {}.  Packing instead.'.format(widget))
                widgets[widget][1].pack()

top.add(fmw['tab'][1], text = 'File Manager')
top.add(agw['tab'][1], text = 'Algorithms')
top.add(pdw['tab'][1], text = 'Predicates')
top.add(mvw['tab'][1], text = 'Moves')

agw['move list'][1].insert(END, Test())

top.pack()
print ('Building interface... Done.')

fmv['bundle path'].set('/Users/sean/github/vermiculus/smp/ssa-tool/examples/ind-set.ssax')
fmf['refresh']()

#root.mainloop()

# Local Variables:
# python-shell-interpreter: "python3"
# python-indent-offset: 4
# End:
