# Dicke State 的準備

產生多體量子糾纏態 Dicke State 的量子線路，參考論文 Deterministic Preparation of Dicke States 方法實作。

---

本專案目的是提供快速簡潔的方法來產生多體糾纏態Dicke State，使用者僅需呼叫函式即可獲得量子線路，並可對其進行測量、計數、後續的量子線路操作。

## Install
```
conda install --file requirements.txt
```
## Usage


### 得到量子線路
```
from DickeState import DickeState

token = your ibm account token
d = DickeState(n=5,k=3,token=None,backend=sim)
d.get_qc()
```
![alt text](resources/image.png)

### 測量
```
d.measure()
d.count(shots=1000)
```
![alt text](resources/image-2.png)

### 測量圖表化
```
d.draw_bar()
```
![alt text](resources/Figure_1.png)