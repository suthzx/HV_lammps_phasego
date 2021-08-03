#thsu0407@gmail.com


8.3早
######温度修改区间！！！

phasego的输入文件格式大改！！！



workflow of alloy ~ phase ...
-----------------------------------------------------
脚本分为三部分，分别为：
lamm.part1  脚本运行  w1.bash
lamm.part2  脚本运行  w2.bash
gotophase   命令行运行

step1
	1.准备当前体系的输入文件demo
	2.当前体系的势场文件
	3.当前服务器提交脚本，提交参数修改：体系in文件的名字
step2
	lamm.part1中 的 Vlist 参数，为体系测试得到的list
step3
	lamm.part2中 的 Vlist 参数，为体系测试得到的list
step4
	gotophase 中 的 alist 参数，为体系测试得到的list
step5
    得到所有输出文件，运行phasego
------------------------------------------------------