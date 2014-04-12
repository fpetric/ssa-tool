from gui.util import *

pdv = dict()
pdf = dict()
pdw = dict()

current_predicate = None

def sel_new(x):
    pdf['screen to bundle']()
    print('switching from ' + (current_predicate.name if current_predicate else '(none)'))
    global current_predicate
    w = pdw['list'][1]
    sel_pd = w.get(w.curselection())
    current_predicate = bundle.lookup(core.Predicate, sel_pd)

    if not current_predicate:        # a new entity was made
        current_predicate = core.Predicate()
        for attr in ['name', 'author', 'date', 'description', 'filename', 'tex', 'definition']:
            setattr(current_predicate, attr, '<%s>' % attr)
        current_predicate.date = '2014-01-01'
        bundle.entities.add(current_predicate)

    pdf['bundle to screen']()

def scr2bdl():
    if not current_predicate:
        return
    from datetime import datetime
    current_predicate.name        = pdv['name'].get()
    current_predicate.author      = pdv['author'].get()
    current_predicate.date        = datetime.strptime(pdv['date'].get(), '%Y-%m-%d')
    current_predicate.filename    = pdv['file'].get()
    current_predicate.description = pdv['description'].get()
    current_predicate.tex         = pdv['tex'].get()
    current_predicate.definition  = [l+'\n' for l in pdw['definition'][1].get(1.0, END).split('\n')[:-2]]

def clrscr():
    pdv['name'        ].set('')
    pdv['author'      ].set('')
    pdv['date'        ].set('')
    pdv['file'        ].set('')
    pdv['description' ].set('')
    pdv['tex'         ].set('')
    try:
        pdw['definition'  ][1].delete(1.0, END)
    except:
        pass

def bdl2scr():
    pdv['name'        ].set(current_predicate.name)
    pdv['author'      ].set(current_predicate.author)
    pdv['file'        ].set(current_predicate.filename)
    pdv['description' ].set(current_predicate.description)
    pdv['tex'         ].set(current_predicate.tex)
    if hasattr(current_predicate.date, 'date'):
        pdv['date'        ].set(current_predicate.date.date())
    else:
        pdv['date'        ].set(current_predicate.date)
    try:
        pdw['definition'][1].delete(1.0, END)
    except:
        pass
    pdw['definition'  ][1].insert(1.0, ''.join(current_predicate.definition))
    pdw['definition'  ][1].do_hl()

def update_name():
    new_name = pdv['name'].get()
    if new_name != current_predicate.name:
        # BUG: crashes if a word is deleted (as opposed to a single character)
        current_predicate.name = new_name
        w = pdw['list'][1]
        idx = w.curselection()
        w.delete(idx)
        w.insert(idx, new_name)
        w.activate(idx)
        w.selection_set(idx)

def sanitize_file():
    old = pdv['file'].get()
    new = old.replace(' ', '-') + ('.py' if not old.endswith('.py') else '')
    pdv['file'].set(new)

pdf['add']              = add_new(pdw, 'list', core.Predicate)
pdf['remove']           = del_sel(pdw, 'list')
pdf['on select new']    = sel_new
pdf['bundle to screen'] = bdl2scr
pdf['screen to bundle'] = scr2bdl
pdf['clear screen']     = clrscr
pdf['update name']      = update_name
pdf['sanitize file']    = sanitize_file

pdv['name']        = StringVar(root)
pdv['file']        = StringVar(root)
pdv['author']      = StringVar(root)
pdv['date']        = StringVar(root)
pdv['description'] = StringVar(root)
pdv['tex']         = StringVar(root)

pdv['name'].trace('w', lambda n, i, m: pdf['update name']())
pdv['file'].trace('w', lambda n, i, m: pdf['sanitize file']())

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
pdw['definition']  = (180 ,  80) , new(SourceText,    pdw, 'tab' , width = 80, height = 16)

bind(pdw, 'list', '<<ListboxSelect>>', pdf['on select new'])

def finalize():
    w = pdw['list'][1]
    p = w.get(ACTIVE)
    w.selection_set(ACTIVE)
    current_predicate = bundle.lookup(core.Predicate, p)
    print (current_predicate)

pdf['finalize'] = finalize

# Local Variables:
# truncate-lines: t
# End:
