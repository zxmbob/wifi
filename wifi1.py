import subprocess
import os
import time
import random

def get_available_wifi_networks():
    """
    获取可用的Wi-Fi网络列表

    返回:
        list: 可用的Wi-Fi网络列表
    """
    try:
        subprocess.run('chcp 65001', shell=True)  # 将控制台代码页更改为UTF-8
        output = subprocess.run(['netsh', 'wlan', 'show', 'network'], capture_output=True, text=True)
        networks = output.stdout.split('\n')
        networks = [line.strip() for line in networks if 'SSID' in line]
        networks = [line.split(':')[1].strip() for line in networks]
        return networks
    except subprocess.CalledProcessError as e:
        print("获取可用的Wi-Fi网络失败。")
        print("错误:", e)
        return []

def connect_to_wifi(ssid, profile_name):
    """
    连接到指定的Wi-Fi网络

    参数:
        ssid (str): 要连接的网络的SSID（Wi-Fi名称）
        profile_name (str): 连接尝试中要使用的配置文件的名称

    返回:
        bool: 如果连接成功则为True，否则为False
    """
    try:
        subprocess.run(['netsh', 'wlan', 'connect', 'name=' + profile_name, 'ssid=' + ssid])
        print("已连接到Wi-Fi网络:", ssid)
        return True
    except subprocess.CalledProcessError as e:
        print("连接到Wi-Fi网络失败:", ssid)
        print("错误:", e)
        return False

def read_passwords_from_file(filename):
    """
    从文件中读取密码列表

    参数:
        filename (str): 包含密码的文件名

    返回:
        list: 密码列表
    """
    try:
        with open(filename, 'r') as file:
            passwords = file.readlines()
    except FileNotFoundError:
        print("密码文件未找到:", filename)
        return []

    passwords = [password.strip() for password in passwords]
    return passwords

def main():
    """
    主函数，获取用户输入并连接到Wi-Fi网络
    """
    available_networks = get_available_wifi_networks()
    if not available_networks:
        print("没有可用的Wi-Fi网络。")
        return

    print("可用的Wi-Fi网络:")
    for i, network in enumerate(available_networks):
        print(f"{i+1}. {network}")

    try:
        network_choice = int(input("请输入要连接的Wi-Fi网络的编号: "))
        if network_choice < 1 or network_choice > len(available_networks):
            print("无效的网络选择。")
            return
    except ValueError:
        print("无效的网络选择。")
        return
    
    ssid = available_networks[network_choice - 1]
    profile_name = input("请输入连接时要使用的配置文件名称: ")

    if not ssid:
        print("SSID不能为空。")
        return

    if not profile_name:
        print("配置文件名称不能为空。")
        return
    
    passwords_file = input("请输入包含密码的文件名: ")

    if not os.path.isfile(passwords_file):
        print("密码文件不存在。")
        return

    passwords = read_passwords_from_file(passwords_file)

    connected = False
    for password in passwords:
        connected = connect_to_wifi(ssid, profile_name)
        if connected:
            break

        # 添加3-5秒的延迟
        delay = random.uniform(3, 5)
        time.sleep(delay)

    if not connected:
        print("无法连接到Wi-Fi网络:", ssid)

if __name__ == '__main__':
    main()
