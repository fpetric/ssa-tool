from gui.util import *

pdv = dict()
pdf = dict()
pdw = dict()

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

# Local Variables:
# truncate-lines: nil
# End:
