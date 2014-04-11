from gui.util import *

agv = dict()
agf = dict()
agw = dict()

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

# Local Variables:
# truncate-lines: nil
# End:
