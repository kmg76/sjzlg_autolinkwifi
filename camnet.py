import re
import time
import os
import requests

# 这里是你的手机号
mobile = ''

# 这里是你的登录密码
passwd = ''

# 设备被服务器踢出后获取不到百度任何数据
# 设备认证后用户自主注销或被挤掉能获取到百度数据
device = 0
while True:
    if not mobile or not passwd:
        break


    # 判断信息
    def baidu_infor():
        # 获取到的百度数据为空时跳出本次循环
        if not get_baidu_str:
            print("=" * 42)
            print("获取到的百度数据为空")
            print("=" * 42)
            return "continue"

        # 能获取到百度信息就跳出本次循环
        if "200 OK" in get_baidu_str:
            print("=" * 42)
            print("获取到百度数据")
            print("=" * 42)
            return "continue"

        # 获取到1.1.1.3的ip就输出剩余分钟并跳出本次循环
        if "1.1.1.3" in get_baidu_str:
            print("=" * 42)
            print("检测到网络临时禁止登录")
            conet = 0
            for i in range(len(get_baidu_arr)):
                if 'Location' in get_baidu_arr[i]:
                    conet = i
            tm = re.search('(?<==).*', get_baidu_arr[conet])
            sp_tm = tm.group()
            print(f"还剩{sp_tm}分钟")
            print("=" * 42)
            return "continue"


    # 请求登录
    def get_user():
        # 获取用户信息所在下标
        num = 0
        for i in range(len(get_user_arr)):
            if "Location" in get_user_arr[i]:
                num = i
        # 正则表达式获取用户IP
        UIP = re.search(
            '(?<=userip=)(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)',
            get_user_arr[num])
        UseIP = UIP.group()

        # 正则表达式获取用户转发IP
        NIP = re.search(
            '(?<=nasip=)(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)',
            get_user_arr[num])
        NasIP = NIP.group()

        # 正则表达式获取用户MAC地址
        UMac = re.search('(?<=user-mac=).*', get_user_arr[num])
        UserMac = UMac.group()

        # 请求主体
        se = requests.Session()
        url = 'http://61.240.137.242:8888/hw/internal_auth'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '425',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': '61.240.137.242:8888',
            'Origin': 'http://61.240.137.242:8888',
            'Referer': 'http://61.240.137.242:8888/hw/HBHUAWEI/login?apmac=11-11-11-11-11-11&userip=' + UseIP + '&nasip=' + NasIP + '&user-mac=' + UserMac,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        }
        data = {
            'mobile': mobile,
            'mobil_english': '',
            'password': passwd,
            'password_english': '',
            'remember_me': '1',
            'auth_type': 'account',
            'enterprise_id': '51',
            'enterprise_url': 'HBHUAWEI',
            'site_id': '4662',
            'client_mac': UserMac,
            'nas_ip': NasIP,
            'wlanacname': 'None',
            'user_ip': UseIP,
            '3rd_ip': 'None',
            'ap_mac': 'None',
            'vlan': '11-11-11-11-11-11',
            'ssid': 'None',
            'ip': 'None',
            'ac_ip': 'None',
            'from': 'None',
            'sn': 'None',
            'gw_id': 'None',
            'gw_address': 'None',
            'url': 'None',
            'language_tag': '0',
        }
        # 发送请求
        content = se.post(url, data=data, headers=headers)
        return content.text


    # 主体开始

    time.sleep(10)

    # 获取百度网页数据,数组格式
    get_baidu_arr = os.popen('curl -i www.baidu.com').readlines()
    # 定义一个百度网页数据的字符串格式
    get_baidu_str = ""

    # 将百度数组转为字符串格式
    for i in range(len(get_baidu_arr)):
        for j in get_baidu_arr[i]:
            get_baidu_str += j

    print("=" * 42)
    print("获取到的百度网页数据:")
    print(get_baidu_str)
    print("=" * 42)

    if baidu_infor() == "continue":
        continue

    # 开始登录
    print(f"当前次数为{device}")
    while device == 0:
        test_user_arr = os.popen('curl -m 10 10.254.0.1 -i').read()
        if "Location: http://61.240.137.242:8888/hw/HBHUAWEI/login?" in test_user_arr:
            print("关键字存在指定数据段中")
            time.sleep(10)
            break
        else:
            print("关键字不存在指定数据段中")
            time.sleep(10)
            continue
    # 请求获取设备登录信息,数据类型为数组
    get_user_arr = os.popen('curl -m 10 10.254.0.1 -i').readlines()
    # 定义一个字符串格式的设备登录信息
    get_user_str = ""

    for i in range(len(get_user_arr)):
        for j in get_user_arr[i]:
            get_user_str += j

    # 获取到异常信息
    # if "8888" in get_user_str:
    #     print("=" * 42)
    #     print("获取到10.254.0.1的数据,5分钟后重启")
    #     print("=" * 42)
    #     time.sleep(300)
    #     os.system('reboot')

    # 请求登录
    if "302" in get_user_str:
        print("=" * 42)
        print("设备没有被登录，请求登录")
        re_info = get_user()
        if "502" in re_info:
            print(re_info)
            print("请求登录成功")
            device += 1
        elif "error" in re_info:
            print("请求登录过于频繁")
            time.sleep(1800)
        else:
            print("请求登录失败")
            print(re_info)
        print("=" * 42)
    # else:
    #     print("=" * 42)
    #     print("设备已登录认证")
    #     print("=" * 42)
