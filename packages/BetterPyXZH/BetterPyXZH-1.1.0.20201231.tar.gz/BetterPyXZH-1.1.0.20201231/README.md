# BetterPy
Use Something to Make Python Better Together!<br><br>
### V1.1.0.20201231:
V1.1.0.20201231:更改_PLUS()为_COMPUTE(),修复了一点BUG.<br>
betterpyInfo()打印程序信息<br>
_BK(<提示信息>)设置程序中断<br>
_DEBUG(<一个或多个变量>)输出变量信息并中断<br>
_QUIT(<提示信息>)中断并退出<br>
_COMPUTE(<变量a>,<运算符>,<变量b>,<可选:输出普通计算结果>)高精度加法.当运算符非"+"或"-"时,会引发ValueError<br>
_RUN_CLOCK(<代码>)执行代码并计算运行所耗时间<br>
_CASE(<变量>,<目标字典>)当变量等于字典中的某个键时,执行该键对应的值.例:_CASE(1,{1:'print("1")',2:'print("2")'})的输出为:1.当变量不在目标字典的范围内时，会引发KeyError<br>
_HELP(<函数名>)输出该函数对应的帮助.当函数名不在模块的范围内时，会引发KeyError<br>

##### Github代码位置:master分支
Happy World!(划掉) Happy New Year!