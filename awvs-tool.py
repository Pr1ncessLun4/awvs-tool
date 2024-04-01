import requests
import json
import time
requests.packages.urllib3.disable_warnings()    #消除警告

exist_targets=[]  #添加目标前已存在的目标
exist_id=[]     #已存在目标id
targets_in_file=[]  #从文件中读取的目标
targets_id=[]       #添加到任务里对应的id
real_targets=[]  #去除已经扫描过的目标
speed='fast'

url="https://127.0.0.1:13443"
url1=url+"/api/v1/targets"
stats_url=url+"/api/v1/me/stats"
speed_url=url+"/api/v1/targets/{}/configuration"
scans_url=url+"/api/v1/scans"
api_key="your-api-key"
headers={'X-Auth':api_key,'content-type':'application/json'}

r1=requests.get(url=url1,headers=headers,verify=False).json()
targets=r1['targets']
for target in targets:
    address=target['address']
    target_id=target['target_id']
    #print(address)
    exist_id.append(target_id)
    exist_targets.append(address)

with open("targets.txt","r") as file:
    f=file.readlines()
    for i in f:
        targets_in_file.append(i)

def not_exist(target_url):
    if target_url not in exist_targets:
        return True
    else:
        return False

#添加目标到扫描队列
def add_targets(target_url):
    target_url=target_url.strip('\n') #去除换行符
    if not_exist(target_url):
        add_data=json.dumps({'address':target_url,'description' : target_url,'criticality' : '10'})
        add_target_res=requests.post(url=url1,headers=headers,data=add_data,verify=False)
        if add_target_res.status_code==201:
            print(target_url+" 添加成功")
        else:
            if len(target_url)!=1 and len(target_url)!=0:
                print(target_url+" 添加失败")
    else:
        print(target_url+" Already exist")

#获取未扫描的目标的id和url
def get_id_address():
    r1=requests.get(url=url1, headers=headers, verify=False).json()
    targets=r1['targets']
    for target in targets:
        if target['last_scan_id'] == None:
            targets_id.append(target['target_id'])
            real_targets.append(target['address'])

#用于控制同时进行扫描的任务数量
def check():
    try:
        while True:
            stats_res=requests.get(url=stats_url,headers=headers,verify=False).json()
            print("Totoal targets: "+str(stats_res['targets_count']))
            print("Scanning targets: "+str(stats_res['scans_running_count']))
            if int(stats_res['scans_running_count'])<1:
                return True
            else:
                return False
    except Exception as e:
        pass
#开始扫描
def scan(id):
    set_data=json.dumps({'scan_speed': speed})
    scan_data=json.dumps({"target_id": id,"profile_id":"11111111-1111-1111-1111-111111111111",
                          "schedule": {'disable':False,'start_date': None,'time_sensitive': False}})
    set_speed_res=requests.patch(url=speed_url.format(id),data=set_data,headers=headers,verify=False)  # 设置扫描速度
    if set_speed_res.status_code==204:  #判断状态码是否为204
        scan_target_res=requests.post(url=scans_url,data=scan_data,headers=headers,verify=False)  # 启动扫描任务
        if scan_target_res.status_code==201:  #判断状态码是否为201
            print(scan_target_res.json()['target_id']+" Running.....")
        else:
            print("任务建立失败")

#添加目标到扫描队列
for target in targets_in_file:
    add_targets(target)
    time.sleep(0.5)
print("添加完毕")
get_id_address()
waiting=len(targets_id)
for t in targets_id:
    while True:
        time.sleep(10)
        if check():
            print("Waiting targets:"+str(waiting))
            scan(t)
            waiting-=1
            break
        print("Waiting targets:" + str(waiting))