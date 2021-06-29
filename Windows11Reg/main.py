import win32api
import win32con


def useWin10(key):
    """
    使用Windows10 开始菜单
    :param key: 注册表句柄
    """
    try:
        win32api.RegSetValueEx(key, 'Start_ShowClassicMode', 0, win32con.REG_DWORD, 1)
        value = win32api.RegQueryValueEx(key, 'Start_ShowClassicMode')
        if value[0] == 1:
            print('设置成功')
        else:
            print('设置失败')
    except Exception as e:
        print(e)
        print('设置失败')


def cancelUseWin10(key):
    """
    删除目标键
    :param key: 注册表句柄
    """
    try:
        win32api.RegSetValueEx(key, 'Start_ShowClassicMode', 0, win32con.REG_DWORD, 0)
        value = win32api.RegQueryValueEx(key, 'Start_ShowClassicMode')
        if value[0] == 0:
            print('设置成功')
        else:
            print('设置失败')
    except Exception as e:
        print('设置失败')
        print(e)


if __name__ == '__main__':
    print('1. Windows 11 取消使用 Windows 10 开始菜单')
    print('2. Windows 11 使用 Windows 10 开始菜单')
    select = int(input('选择：'))
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,
                              'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced', 0,
                              win32con.KEY_ALL_ACCESS)
    if select == 1:
        cancelUseWin10(key)
    elif select == 2:
        useWin10(key)

    win32api.RegCloseKey(key)
