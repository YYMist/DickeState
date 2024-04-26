from DickeState import DickeState

d = DickeState(n=5,k=3,token=None,backend=None)
d.get_qc()
d.measure()
d.count(shots=1000)
d.draw_bar()