# mdbridge

markdown extension for bridge

这里是研究如何从markdown格式的桥牌文章转换到HTML（拷贝到Word）和PDF（通过LaTeX或者epub）

最新结果

* 通过扩展的markdown格式能够产生希望的HTML（`xin2pbn`,`pbn2html`,`mdbridge`三个软件包）
* 通过`pandoc`软件能够产生epub
* `calibre`能够转换出mobi和pdf格式

存在的问题

* HTML还不太规范，epub产生出来有错，mobi格式有瑕疵
* HTML拷贝到word还不是很好
* epub到PDF后红花牌颜色不对，目录没有
* latex (onedown）还没试

## 如何工作

````
# sample.md
<pre lang="bridge">
deal|cards=NS|ul="<str>"|ll=<str>|ur=<str>`
</pre>
$ pip install mdbridge
$ mdbridge2html sample.md
sample.bridge is created
# pandoc
$ pandoc -f markdown+raw_attribute -t epub epub.txt sample.bridge -o sample.epub
# multimarkdown
$ multimarkdown sample.bridge > sample.html
````

### 叫牌

<pre lang="bridge">
http://www.xinruibridge.com/deallog/DealLog.html?bidlog=P,2N,P%3B3C,P,3N,P%3B6N,P,P,P%3B&playlog=E:KD,3D,4D,JD%3BE:2D,5D,7D,AD%3BN:JS,6S,5S,8S%3BN:KS,4S,7S,2S%3BN:3S,TS,AS,8H%3BS:QS,TD,4C,9S%3BS:KH,JH,4H,2H%3BS:AH,TH,9H,3H%3BS:QH,9D,8C,5H%3BS:2C,JC,QC,6C%3BN:KC,9C,6D,5C%3BN:AC,7H,6H,3C%3BN:7C,QD,8D,TC%3B&deal=82.JT8.T974.JT53%20KJ3.94.AJ.AKQ874%20T964.7532.KQ2.96%20AQ75.AKQ6.8653.2&vul=All&dealer=W&contract=6N&declarer=N&wintrick=11&score=-100&str=%E7%BE%A4%E7%BB%84IMP%E8%B5%9B%2020201209%20%E7%89%8C%E5%8F%B7%204/8&dealid=995050099&pbnid=345464272
auction
</pre>

### 牌

`deal|cards=NS|ul="<str>"|ll=<str>|ur=<str>`

* deal: 四家牌，从西开始SHDC，`-`:无关紧要，`x`: 小牌
* cards: 南北（NS），西北（WN）: 缺省就是四家
* ul/ur/ll: 三个角(u=upper,r=right,l=left,l=lower)，`&`用来换行 ，上左角（ul）缺省有显示，用`" "`隐藏, ``

两家牌

<pre lang="bridge">
deal|cards=NS
</pre>

四家牌

<pre lang="bridge">
deal
</pre>

部分牌

<pre lang="bridge">
deal=.xxxx..xxx&.T4.A.AK87&-&.AKQ6.865.
</pre>

两家牌 （不显示定约）

<pre lang="bridge">
deal|cards=NS|ul=NONE 
</pre>

部分牌 （显示当前赢墩）

<pre lang="bridge">
deal=.xxxx..xxx&.94.A.AK87&-&.AKQ6.865.|ll="NS 4/12&EW 0"|ur="群组赛1209&牌号 4/8"
</pre>


