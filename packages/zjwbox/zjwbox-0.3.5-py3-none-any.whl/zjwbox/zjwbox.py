from dataclasses import dataclass
from collections import Counter
from zjwbox.boxtools.alert_exit import alertExit
from datetime import datetime
import json, re, requests



# 处理特殊字符串
def deal_string(pre_string: str) -> str:
    if '_' in pre_string:
        return pre_string.replace("_", " ")
    return pre_string

translator_num=392
def translator(string: str) -> str:
    """
    input : string 需要翻译的字符串
    output：translation 翻译后的字符串
    有每小时1000次访问的限制
    """
    string = deal_string(string)
    global  translator_num
    translator_num = translator_num + 1
    # API
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数， i为要翻译的内容
    key = {
        'type': "AUTO",
        'i': string,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 通过 json.loads 把返回的结果加载成 json 格式
        result = json.loads(response.text)
#         print ("输入的词为：%s" % result['translateResult'][0][0]['src'])
#         print ("翻译结果为：%s" % result['translateResult'][0][0]['tgt'])
        translation = result['translateResult'][0][0]['tgt']
        return translation
    else:
        print("有道词典调用失败")
        # 相应失败就返回空
        return None
    



@dataclass
class Infer(object):
    data_type: str
    
    def __str__(self):
        info =         """
        welcome you!
        This is a class that improve infer!
        You must give it a arg to str type, "list", "tuple" or "set".
        """
        return info
    
    def __getitem__(self, key):
        if len(str(key)) < 2:
            print("语法错误：输入格式数不能少于2！")
            return
        if isinstance(key, tuple) and len(key) in (2, 3, 4) and (key[2] is Ellipsis or key[1] is Ellipsis or key[3] is Ellipsis):
            if key[1] is Ellipsis:
                basic_infer = [i for i in range(key[0], key[-1] + 1)]
            elif key[3] is Ellipsis:
                basic_infer = [i for i in range(key[0], key[-1] + 1, key[1] - key[0])]
            else:
                basic_infer = [i for i in range(key[0], key[-1] + 1, key[1] - key[0])]
            
            if self.data_type == "list":
                return basic_infer
            if self.data_type == "tuple":
                return tuple(basic_infer)
            if self.data_type == "set":
                return set(basic_infer)
        timers = Counter(self.data_type).most_common()
        for timer in timers:
            if 2 in timer:
                print(f"请检查参数: {self.data_type}\n参考参数：'list', 'tuple', 'set'！")
                return
        if len(self.data_type) < 3 or len(self.data_type) > 5:
            print(f"请检查参数: {self.data_type}\n参考参数：'list', 'tuple', 'set'！")
        else:
            print(None)
                

alertExit()


# if __name__ == "__main__":
#     p = Infer("set")
#     print( p[1, 5,  ...,100] )

