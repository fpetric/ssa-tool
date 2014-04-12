from gui.util import *

mvv = dict()
mvf = dict()
mvw = dict()

current_move = None

def sel_new(x):
    global current_move
    w = mvw['list'][1]
    sel_mv = w.get(w.curselection())
    current_move = bundle.lookup(core.Move, sel_mv)

    mvv['name'        ].set(current_move.name)
    mvv['author'      ].set(current_move.author)
    mvv['date'        ].set(current_move.date)
    mvv['file'        ].set(current_move.filename)
    mvv['description' ].set(current_move.description)
    mvv['tex'         ].set(current_move.tex)

mvf['add']         = add_new(mvw, 'list', core.Move)
mvf['remove']      = del_sel(mvw, 'list')
mvf['on select new'] = sel_new

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

bind(mvw, 'list', '<<ListboxSelect>>', mvf['on select new'])

# Local Variables:
# truncate-lines: nil
# End:
