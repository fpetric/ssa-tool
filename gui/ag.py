# (setq-default truncate-lines t)
from gui.util import *
from gui import bundle

agv = dict()
agf = dict()
agw = dict()

agv['current algorithm'] = None
agv['current rule'] = None

def dd():
    for v in ['current algorithm', 'current rule']:
        print('\t', v, agv[v])
    if agv['current rule']:
        print('\t algorithm rules:', agv['current algorithm'].rules)

def new_algorithm():
    print('inside new_algorithm()')
    agv['current algorithm']        = core.Algorithm()
    agv['current algorithm'].name   = '<name>'
    agv['current algorithm'].author = '<author>'
    agv['current algorithm'].date   = '<date>'
    agv['current algorithm'].rules  = list()
    agv['current rule']             = None
    bundle.entities.add(agv['current algorithm'])
def new_rule():
    print('inside new_rule()')
    agv['current rule']             = core.Rule()
    agv['current rule'].name        = '<name>'
    agv['current rule'].author      = '<author>'
    agv['current rule'].date        = '2014-01-01'
    agv['current rule'].predicate   = core.Predicate(name='<predicate>')
    agv['current rule'].moves       = []
    print('appending new rule')
    agv['current algorithm'].rules.append(agv['current rule'])
    dd()



def a_onsel(event, override = False):
    print('inside a_onsel(event):', event)
    '''
    on select new algorithm, save the existing
    information and load the new information
    '''
    if not override and agv['current algorithm']: a_scr2bdl()
    w = get(agw, 'algorithm list')
    n = w.get(w.curselection())
    agv['current algorithm'] = bundle.lookup(core.Algorithm, n)
    a_bdl2scr()



def r_onsel(event, override=False):
    print('inside r_onsel(event):', event)
    if not override and agv['current rule']: 
        print('doing s2b')
        r_scr2bdl()
    w = get(agw, 'rule list')
    n = w.get(w.curselection())
    print('## selection was', n)
    dd()
    agv['current rule'] = agv['current algorithm'].lookup(n)
    r_bdl2scr()



def a_bdl2scr():
    print('inside a_bdl2scr()')
    '''
    creates a new algorithm if necessary,
    and copies the algorithm data
    into the graphical interface.

    this algorithm data includes rule names for the list,
    but the population from this list is left to r_bdl2scr.
    '''
    if not agv['current algorithm']:
        new_algorithm()
    agv['algorithm name'   ].set(agv['current algorithm'].name   )
    agv['algorithm date'   ].set(agv['current algorithm'].date   )
    agv['algorithm author' ].set(agv['current algorithm'].author )
    get(agw, 'move list').delete(0, END)
    get(agw, 'move list for rule').delete(0, END)
    rl = get(agw, 'rule list')
    rl.delete(0, END)
    for r in agv['current algorithm'].rules:
        rl.insert(END, r.name)



def a_scr2bdl():
    print('inside a_scr2bdl()')
    '''
    copies data from the interface into the underlying algorithm.
    '''
    if not agv['current algorithm']: return
    agv['current algorithm'].name   = agv['algorithm name'   ].get()
    agv['current algorithm'].author = agv['algorithm author' ].get()
    agv['current algorithm'].date   = agv['algorithm date'   ].get()
    if agv['current rule']: r_scr2bdl()



def r_bdl2scr():
    print('inside r_bdl2scr()')

    agv['rule name'      ].set(agv['current rule'].name      )
    agv['rule author'    ].set(agv['current rule'].author    )
    agv['rule date'      ].set(agv['current rule'].date      )
    agv['rule predicate' ].set(agv['current rule'].predicate.name )

    get(agw, 'move list').delete(0, END)
    get(agw, 'move list for rule').delete(0, END)

    for m in bundle.types(core.Move):
        lb = get(agw, 'move list for rule'
                      if m in agv['current rule'].moves
                      else 'move list')
        lb.insert(END, m.name)



def r_scr2bdl():
    print('inside r_scr2bdl()')
    agv['current rule'].name      = agv['rule name'      ].get()
    agv['current rule'].author    = agv['rule author'    ].get()
    agv['current rule'].date      = agv['rule date'      ].get()
    agv['current rule'].predicate = bundle.lookup(core.Predicate, agv['rule predicate' ].get())

a_update_name = name_updater(agw , agv , 'algorithm list' , 'algorithm name' , 'current algorithm' )
r_update_name = name_updater(agw , agv , 'rule list'      , 'rule name'      , 'current rule'      )

agv['current algorithm' ] = None
agv['current rule'      ] = None
agv['rule predicate'    ] = StringVar(root)
agv['algorithm name'    ] = StringVar(root)
agv['algorithm author'  ] = StringVar(root)
agv['algorithm date'    ] = StringVar(root)
agv['rule name'         ] = StringVar(root)
agv['rule author'       ] = StringVar(root)
agv['rule date'         ] = StringVar(root)

def move(lb1, lb2, pre=None, post=None):
    """Moves the ACTIVE item from lb1 to lb2

    lb1 and lb2 are names that are in the widget_dictionary
    """
    def f():
        active = get(agw, lb1).get(ACTIVE)
        if str(active) != '':   # to avoid moving empty items
            if pre: pre()
            get(agw, lb1).delete(ACTIVE)
            get(agw, lb2).insert(END, active)
            if post: post()
    return f

def add_a():
    pass
def del_a():
    pass
def add_r():
    pass
def del_r():
    pass
def add_m():
    active = get(agw, 'move list').get(ACTIVE)
    agv['current rule'].moves.append(bundle.lookup(core.Move, active))
def del_m():
    active = get(agw, 'move list for rule').get(ACTIVE)
    agv['current rule'].moves.remove(bundle.lookup(core.Move, active))

def do_add_alg():
    new_algorithm()
    lb = get(agw, 'algorithm list')
    lb.insert(END, agv['current algorithm'].name)
    try:
        lb.selection_clear(lb.curselection())
    except:
        pass
    lb.selection_set(END)
    
    agv['algorithm name'].set(agv['current algorithm'].name)
    agv['algorithm author'].set(agv['current algorithm'].author)
    agv['algorithm date'].set(agv['current algorithm'].date)

    get(agw, 'rule list').delete(0, END)

agf['add algorithm'     ] = do_add_alg#add_new(agw, 'algorithm list'     , core.Algorithm       , pre = new_algorithm)
def do_add_rule():
    new_rule()
    lb = get(agw, 'rule list')
    lb.insert(END, agv['current rule'].name)
    try:
        lb.selection_clear(lb.curselection())
    except:
        pass
    lb.selection_set(END)
    r_onsel(None, override=True)
    
agf['add rule'          ] = do_add_rule# add_new(agw, 'rule list'          , core.Rule            , pre = new_rule, post=lambda:get(agw, 'rule list').selection_set(END))
agf['delete algorithm'  ] = del_sel(agw, 'algorithm list'                            , pre = del_a)
agf['delete rule'       ] = del_sel(agw, 'rule list'                                 , pre = del_r)
agf['add move'          ] = move   (     'move list'          , 'move list for rule' , pre = add_m)
agf['delete move'       ] = move   (     'move list for rule' , 'move list'          , pre = del_m)

def upd_pr():
    new_val = agv['rule predicate'].get()
    q = bundle.lookup(core.Predicate, new_val)
    agw['rule predicate'][1]['foreground'] = 'black' if q else 'red'
    if q:
        agv['current rule'].predicate = q

agf['upd_pr'] = upd_pr

agw['tab']                =    None ,        Frame(top)
agw['rule group']         = (   165 ,   40), new(Labelframe , agw , 'tab'        ,         text =     'Rules',            height=300, width=775)
agw['name']               = (   165 ,    0), new(Entry      , agw , 'tab'        , textvariable = agv['algorithm name']   )
agw['author']             = (   340 ,    0), new(Entry      , agw , 'tab'        , textvariable = agv['algorithm author'] )
agw['date']               = (   340 ,   25), new(Entry      , agw , 'tab'        , textvariable = agv['algorithm date']   )
agw['rule name']          = (   170 ,    0), new(Entry      , agw , 'rule group' , textvariable = agv['rule name']        )
agw['rule date']          = (   170 ,   25), new(Entry      , agw , 'rule group' , textvariable = agv['rule date']        )
agw['rule author']        = (   170 ,   50), new(Entry      , agw , 'rule group' , textvariable = agv['rule author']      )
agw['rule predicate']     = (   170 ,   75), new(Entry      , agw , 'rule group' , textvariable = agv['rule predicate']   )
agw['alg  add']           = (     0 ,  310), new(Button     , agw , 'tab'        ,         text =     'add'               , command = agf[   'add algorithm'] )
agw['alg  del']           = (    80 ,  310), new(Button     , agw , 'tab'        ,         text =     'del'               , command = agf['delete algorithm'] )
agw['rule add']           = (     0 ,  110), new(Button     , agw , 'rule group' ,         text =     'add'               , command = agf[   'add rule']      )
agw['rule del']           = (    80 ,  110), new(Button     , agw , 'rule group' ,         text =     'del'               , command = agf['delete rule']      )
agw['move add']           = (   140 ,  175), new(Button     , agw , 'rule group' ,         text =     '>'                 , command = agf[   'add move']      )
agw['move del']           = (   140 ,  200), new(Button     , agw , 'rule group' ,         text =     '<'                 , command = agf['delete move']      )
agw['algorithm list']     = (     0 ,    0), new(Listbox    , agw , 'tab'        ,       height = 18                      )
agw['rule list']          = (     0 ,    0), new(Listbox    , agw , 'rule group' ,       height =  6                      )
agw['move list']          = (     0 ,  140), new(Listbox    , agw , 'rule group' ,       height =  7                      )
agw['move list for rule'] = (   200 ,  140), new(Listbox    , agw , 'rule group' ,       height =  7                      )

get(agw, 'algorithm list' ).bind('<<ListboxSelect>>', a_onsel)
get(agw, 'rule list'      ).bind('<<ListboxSelect>>', r_onsel)

agv['algorithm name'].trace('w', lambda n, i, m: a_update_name())
agv[     'rule name'].trace('w', lambda n, i, m: r_update_name())
agv['rule predicate'].trace('w', lambda n, i, m: upd_pr())
agv['rule date'].trace('w', lambda n, i, m: so_done())
agv['rule author'].trace('w', lambda n, i, m: so_done2())

def so_done():
    agv['current rule'].date = agv['rule date'].get()
def so_done2():
    agv['current rule'].author = agv['rule author'].get()

# Local Variables:
# truncate-lines: t
# End:
