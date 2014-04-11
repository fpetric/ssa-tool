print ('Building interface...')

from gui import *

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

#exit()

# Local Variables:
# python-shell-interpreter: "python3"
# python-indent-offset: 4
# truncate-lines: nil
# End:
