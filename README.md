# PC-98 光荣-三国志2日文汉字系统研究和破解

## 背景简介
小时候只玩过智冠的三国演义，据说是在这个游戏的基础上改的，就想体会一下原始版。创建新武将时，发现有些汉字是游戏里有的，但是游戏提供的输入法里找不到，比如游戏人物里用的'贾'这个字。
在存档里按智力武力魅力的方法，很快找到几个武将的位置，发现他们的名字都是安装日文Shift JIS编码存的，于是先找到自己想要的字的JIS码，再直接编辑这个存档文件，把人物名字改掉就好。
但是很快发现两个问题：
1. 有些字找不到对应的JIS码，比如蒋琬的'琬'
2. 有些字有JIS码但是游戏里显示成☆，比如妲己的‘妲’，JIS码9B46
<img width="878" height="108" alt="05" src="https://github.com/user-attachments/assets/e82b9d10-d215-4c66-9520-0877b1a98b02" />

<img width="664" height="136" alt="03" src="https://github.com/user-attachments/assets/ab1e40d7-f61f-4679-9ecb-6da33d8fabb8" />

<img width="637" height="392" alt="01" src="https://github.com/user-attachments/assets/612e0a96-3b14-4791-a4b6-105d960ae5e2" />

于是就想研究一下这个游戏到底是怎么显示日文汉字，另外如何解决缺字的问题。

## 分析和破解过程
首先注意到游戏的A盘里有一个FONT.DAT的文件，但是大小只有3k左右，按那个年代常用的16x16或者16x14的字模也存不了多少(大概100-200之间)。
于是先用Pyython写了一个脚本（dump_font_jp.py），把这个FONT.DAT里有的字先打印出来看看:

<img width="2048" height="256" alt="font16_sheet-0" src="https://github.com/user-attachments/assets/ad933d48-4620-4d4b-a596-40d3e77193aa" />

发现值得注意的几点：
1. 一共收录137个字，其中大部分有JIS码，少部分没有对应的JIS码，比如'诩'，'琬'，'♥'，有JIS码的大都排在前面，没有JIS码的一定都跟在后面
2. 有JIS码的情况，游戏里基本也在用同样的JIS码，比如98A1(丕)，E9B0(魏)，不过有个别例外比如FA63(昱)，如果用JIS码则游戏显示<img width="16" height="15" alt="x" src="https://github.com/user-attachments/assets/9399c1a4-8b64-4879-88e4-f457744bb40d" />

查了下资料，游戏发售时的平台是PC-8801，支持JIS第一水准汉字，也就是889F(亜)到9872(腕)，之后的第1水准汉字从989F(弌)开始，游戏从JIS码9873开始显示空白，而989F前面几个码(如989E)显示☆(JIS码8199)，所以估计界限在中间某个值，程序检查超过这个值就去找FONT.DAT里的汉字，再没有就显示☆，之前的因为没超过界限值，也没有对应的汉字才显示空白。
估计当年的游戏开发者把游戏需要用到的其他汉字放进这个FONT.DAT，这个FONT.DAT的字库前面先排JIS码有的(第2水准汉字)，后面再排JIS码没有的，FA63(昱)看地址应该是JIS码后来再扩充的，可能游戏制作时JIS码还没收录。前面有JIS码的在游戏里还采用JIS编码，后面没有JIS码的用游戏内部自定的编码。
从中间开始查，很快就得到FONT.DAT中收录的JIS码汉字最后一个是E9B8(鮑)，后面跟着的'瓒'没有JIS编码，根据人物公孙瓒的数值查存档文件发现这个字用的游戏内部编码是EB9F，后面的每个字编码+1，实测基本证实这个猜想，有个别例外，比如最后的'琬'是EBC7，而它前面一个值EBC6显示<img width="16" height="15" alt="x" src="https://github.com/user-attachments/assets/9399c1a4-8b64-4879-88e4-f457744bb40d" />，猜测是之前有一个字，但是后来被拿掉了，或者是加字时把码搞错了，这个137的字库里有重复的，所以不排除不同的人分别加的，但最后没整合好。

## 解决方案
既然这个FONT.DAT有重复的字，最简单的方法就是换掉其中一个，有两个选择'琮'和'琬'。查了一下游戏的资料，这两个字分别用在:
蒋琬(EBB8) 黄琬(EBC7)
刘琮(EBC1) 全琮(EBBA)
最后选择替换掉琮(EBC7)，两个原因，第一是EBC7的'琮'FONT.DAT字库里是最后一个，这样方便将来也好记，另外就是黄琬只在前两个时代剧本中出现，相关的改动少。

## 具体操作过程
1. 写一个Python脚本patch_font.py，用想要的字替换掉FONT.DAT里最后一个字'琬'，打完补丁的FONT.DAT用前面的dump_font_jp.py检查得到(这里采用'妲'字为例)：   
   <img width="2048" height="256" alt="font16_sheet" src="https://github.com/user-attachments/assets/f5d8a223-ad3f-4bae-b693-f89700f1f531" />

2. 修改游戏存档中的人物名字，用码值EBC7代表自己添加的汉字，再进入游戏检查确认正确：
  <img width="640" height="398" alt="daji" src="https://github.com/user-attachments/assets/3fee72ce-ba39-4e41-ac73-5e513e334356" />

3. 修改游戏Disk B上的SNDATA1.CIM和SNDATA2.CIM里黄琬的名字，把他用的'琬'换成蒋琬一样的游戏内部编码EBB8，再进入游戏检查：
  <img width="2560" height="1440" alt="huangwan" src="https://github.com/user-attachments/assets/609fa181-8465-4ecd-be43-709d7653a5e0" />

## 到这里就完成了，Enjoy! 

<img width="671" height="420" alt="貂蝉00" src="https://github.com/user-attachments/assets/cde87a2f-4b9d-4c82-8b4b-1922e4e92d1f" />
