from gui.util import *
from gui import bundle

agv = dict()
agf = dict()
agw = dict()

current_algorithm = None
current_rule = None

def sel_new_rule(x):
    global current_algorithm
    global current_rule

    w = agw['rule list'][1]
    sel_rule = w.get(w.curselection())
    current_rule = current_algorithm.lookup(sel_rule)

    # populate metadata
    if not current_rule:        # a new rule was made
        current_rule = core.Rule()
        for attr in ['name', 'author', 'date', 'description']:
            setattr(current_rule, attr, '<%s>' % attr)
        current_rule.predicate = ''
        current_rule.moves = []
        current_algorithm.rules.append(current_rule)

    agv['rule name'      ].set(current_rule.name)
    agv['rule author'    ].set(current_rule.author)
    agv['rule date'      ].set(current_rule.date)
    if hasattr(current_rule.predicate, 'name'):
        agv['rule predicate' ].set(current_rule.predicate.name)
    else:
        agv['rule predicate' ].set('')


def sel_new_algorithm(x):
    global current_algorithm

    # find selected algorithm
    sel_alg = agw['algorithm list'][1].get(ACTIVE)
    current_algorithm = bundle.lookup(core.Algorithm, sel_alg)

    # populate metadata
    agv['algorithm name'   ].set(current_algorithm.name)
    agv['algorithm author' ].set(current_algorithm.author)
    agv['algorithm date'   ].set(current_algorithm.date)

    # populate rule list
    rule_list = agw['rule list'][1]
    rule_list.delete(0, END)
    for rule in current_algorithm.rules:
        rule_list.insert(END, rule.name)

def upd_alg_name():
    new_name = agv['algorithm name'].get()
    wgt = agw['algorithm list'][1]
    if new_name != current_algorithm.name:
        current_algorithm.name = new_name
        idx = wgt.curselection()
        wgt.delete(idx)
        wgt.insert(idx, new_name)
        wgt.activate(idx)
        wgt.selection_set(idx)
def upd_rule_name():
    new_name = agv['rule name'].get()
    wgt = agw['rule list'][1]
    if current_algorithm and current_rule and new_name != current_rule.name:
        current_rule.name = new_name
        idx = wgt.curselection()
        wgt.delete(idx)
        wgt.insert(idx, new_name)
        wgt.activate(idx)
        wgt.selection_set(idx)
agf['selected different rule']             = sel_new_rule
agf['selected different algorithm']        = sel_new_algorithm
agf['create new algorithm']                = lambda : print('create new algorithm') 
agf['delete this algorithm']               = lambda : print('delete this algorithm') 
agf['create new rule']                     = lambda : print('create new rule') 
agf['delete rule']                         = lambda : print('delete rule') 

agv['rule predicate']     = StringVar(root)
agv['algorithm name']     = StringVar(root)
agv['algorithm author']   = StringVar(root)
agv['algorithm date']     = StringVar(root)
agv['rule name']          = StringVar(root)
agv['rule author']        = StringVar(root)
agv['rule date']          = StringVar(root)

agf['add algorithm']      = add_new(agw, 'algorithm list', core.Algorithm , bind=agf['create new algorithm'])
agf['delete algorithm']   = del_sel(agw, 'algorithm list'                 , bind=agf['delete this algorithm'])
agf['add rule']           = add_new(agw, 'rule list', core.Rule, bind=agf['create new rule'])
agf['delete rule']        = del_sel(agw, 'rule list',            bind=agf['delete rule'])
agf['add move']           = move   (agw, 'move list', 'move list for rule')
agf['delete move']        = move   (agw, 'move list for rule', 'move list')

def upd_pr():
    new_val = agv['rule predicate'].get()
    if bundle.lookup(core.Predicate, new_val):
        agw['rule predicate'][1]['foreground'] = 'black'
    else:
        agw['rule predicate'][1]['foreground'] = 'red'

agf['upd_pr'] = upd_pr

agw['tab']                =    None ,        Frame(top)
agw['rule group']         = (   165 ,   40), new(Labelframe, agw, 'tab', text = 'Rules', height=300, width=775)
agw['name']               = (   165 ,    0), new(Entry,   agw, 'tab',        textvariable = agv['algorithm name'])
agw['author']             = (   340 ,    0), new(Entry,   agw, 'tab',        textvariable = agv['algorithm author'])
agw['date']               = (   340 ,   25), new(Entry,   agw, 'tab',        textvariable = agv['algorithm date'])
agw['rule name']          = (   170 ,    0), new(Entry,   agw, 'rule group', textvariable = agv['rule name'])
agw['rule date']          = (   170 ,   25), new(Entry,   agw, 'rule group', textvariable = agv['rule date'])
agw['rule author']        = (   170 ,   50), new(Entry,   agw, 'rule group', textvariable = agv['rule author'])
agw['rule predicate']     = (   170 ,   75), new(Entry,   agw, 'rule group', textvariable = agv['rule predicate'])
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

agf['update algorithm name']               = upd_alg_name
agf['update rule name']                    = upd_rule_name

bind(agw, 'rule list', '<<ListboxSelect>>', agf['selected different rule'])
bind(agw, 'algorithm list', '<<ListboxSelect>>', agf['selected different algorithm'])
agv['algorithm name' ].trace('w', lambda n, i, m: agf['update algorithm name']())
agv['rule name'      ].trace('w', lambda n, i, m: agf['update rule name']())
agv['rule predicate' ].trace('w', lambda n, i, m: agf['upd_pr']())


def finalize():
    print('finalizing')

agf['finalize'] = finalize

# Local Variables:
# truncate-lines: t
# End:
