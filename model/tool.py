import configparser


def GetConfigData(Section:str,Value:str)->str|None:
    Config=configparser.ConfigParser()
    Config.read('config.ini')
    try:
        return Config[Section][Value]
    except:
        print(f'[ERROR] 無法獲得[{Section}][{Value}]')
        return 