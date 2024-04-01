将源代码中的api_key换成自己的apikey

![image](https://github.com/Pr1ncessLun4/awvs-tool/assets/131739779/c86b0b42-f835-4310-bf3a-6686babb720d)

把目标放到txt文件中(不超过99个，一行一个)
运行：python awvs-tool.py 1.txt
不出意外的话一会儿就能看到awvs框框添加目标，添加完之后会自动开始扫描。这里设置了最大同时扫描数量为1，2G的服务器任务多了会崩掉，有需要可自行更改check函数
![image](https://github.com/Pr1ncessLun4/awvs-tool/assets/131739779/8a34bd0c-b946-4de5-83c1-25e855595bdc)

服务器运行：nohup python awvs-tool 1.txt  服务器没炸就可以没日没夜的跑
