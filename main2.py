from DickeState import DickeState

token = "0ec05f0822a09d58a1c3bf7ac3da9d4b00d51a0b7c3a0dcb6a974f00c6aef059e20bb51e658ab529a4470a33efff7bf2faec50e010dda515587fdd81f5432ddf"
d = DickeState(n=5,k=3,token=None,backend=None)
d.get_qc()
d.measure()
d.count(shots=1000)
d.draw_bar()