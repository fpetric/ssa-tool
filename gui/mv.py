from gui.util import *

mvv = dict()
mvf = dict()
mvw = dict()

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

# Local Variables:
# truncate-lines: nil
# End:
