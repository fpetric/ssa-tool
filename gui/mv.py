from gui.util import *

mvv = dict()
mvf = dict()
mvw = dict()

current_move = None

def sel_new(x):
    mvf['screen to bundle']()
    print('switching from ' + (current_move.name if current_move else '(none)'))
    global current_move
    w = mvw['list'][1]
    sel_mv = w.get(w.curselection())
    current_move = bundle.lookup(core.Move, sel_mv)

    if not current_move:        # a new entity was made
        current_move = core.Move()
        for attr in ['name', 'author', 'date', 'description', 'filename', 'tex', 'definition']:
            setattr(current_move, attr, '<%s>' % attr)
        current_move.date = '2014-01-01'
        bundle.entities.add(current_move)

    mvf['bundle to screen']()

def scr2bdl():
    if not current_move:
        return
    from datetime import datetime
    current_move.name        = mvv['name'].get()
    current_move.author      = mvv['author'].get()
    current_move.date        = datetime.strptime(mvv['date'].get(), '%Y-%m-%d')
    current_move.filename    = mvv['file'].get()
    current_move.description = mvv['description'].get()
    current_move.tex         = mvv['tex'].get()
    current_move.definition  = [l+'\n' for l in mvw['definition'][1].get(1.0, END).split('\n')[:-2]]

def clrscr():
    mvv['name'        ].set('')
    mvv['author'      ].set('')
    mvv['date'        ].set('')
    mvv['file'        ].set('')
    mvv['description' ].set('')
    mvv['tex'         ].set('')
    try:
        mvw['definition'  ][1].delete(1.0, END)
    except:
        pass

def bdl2scr():
    mvv['name'        ].set(current_move.name)
    mvv['author'      ].set(current_move.author)
    mvv['file'        ].set(current_move.filename)
    mvv['description' ].set(current_move.description)
    mvv['tex'         ].set(current_move.tex)
    if hasattr(current_move.date, 'date'):
        mvv['date'        ].set(current_move.date.date())
    else:
        mvv['date'        ].set(current_move.date)
    try:
        mvw['definition'][1].delete(1.0, END)
    except:
        pass
    mvw['definition'  ][1].insert(1.0, ''.join(current_move.definition))

def update_name():
    new_name = mvv['name'].get()
    if new_name != current_move.name:
        # BUG: crashes if a word is deleted (as opposed to a single character)
        current_move.name = new_name
        w = mvw['list'][1]
        idx = w.curselection()
        w.delete(idx)
        w.insert(idx, new_name)
        w.activate(idx)
        w.selection_set(idx)

def sanitize_file():
    old = mvv['file'].get()
    new = old.replace(' ', '-') + ('.py' if not old.endswith('.py') else '')
    mvv['file'].set(new)

mvf['add']              = add_new(mvw, 'list', core.Move)
mvf['remove']           = del_sel(mvw, 'list')
mvf['on select new']    = sel_new
mvf['bundle to screen'] = bdl2scr
mvf['screen to bundle'] = scr2bdl
mvf['clear screen']     = clrscr
mvf['update name']      = update_name
mvf['sanitize file']    = sanitize_file

mvv['name']        = StringVar(root)
mvv['file']        = StringVar(root)
mvv['author']      = StringVar(root)
mvv['date']        = StringVar(root)
mvv['description'] = StringVar(root)
mvv['tex']         = StringVar(root)

mvv['name'].trace('w', lambda n, i, m: mvf['update name']())
mvv['file'].trace('w', lambda n, i, m: mvf['sanitize file']())

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

bind(mvw, 'list', '<<ListboxSelect>>', mvf['on select new'])

# Local Variables:
# truncate-lines: t
# End:
