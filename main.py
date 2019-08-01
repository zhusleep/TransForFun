import pandas as pd
from translator import translate,Kaihua
from tqdm import tqdm as tqdm
import time
js = Kaihua()

success = 0
a_list = ['我的花呗预期了','我的花呗逾期了','苹果7什么时候上市','苹果5什么时候上市','一定要去4S店才能更换后视镜吗？',
          '汽车在升级程序后就无法读取系统这是什么个情况','我都等三个月了','那你们系统是根据什么把我的花呗停掉的',
          '为什么还开不了花呗借呗什么的','北京到广州顺丰快递要多久','顺丰快递广州到北京要多久','尽情花呗是什么情况',
          '尽情花呗如何开','不小心开通花呗','我想开通花呗？不知道怎么操作','给泰迪起什么名字好听','泰迪犬取什么名字好听，是MM！']
# a_list 保存待翻译的句子列表。
a_trans_list = []
# a_trans_list 保存翻译后的句子列表。
"""
总体流程
每100句话用'\n'作为分隔符组成一个文档放入谷歌进行翻译，翻译回来后解析回原来的100句话。
单句单句输入太费时间。如此设计10w短文本的翻译时间大约是20min。
注意，100句话总字数不能超过5000字，这是谷歌翻译的限制。因此可根据文本长度自由调节这个combined_length值.
"""
combined_length = 100
for i in tqdm(range(len(a_list)//combined_length+1)):
    content = '\n'.join(a_list[i*combined_length:(i+1)*combined_length])
    if content=='': continue
    get_trans=True
    while get_trans:
        try:
            tk = js.getTk(content)
            result = translate(content, tk)
            result = result.replace('null','None')
            result = result.replace('true','True')
            result = result.replace('false','False')
            result = eval(result)
            trans_result = ''
            for item in result[0][0:-1]:
                trans_result += item[0]
            train_result = trans_result.split('\n')
            print(len(train_result),len(content.split('\n')))
            if len(train_result)!= len(content.split('\n')):
                print('wrong')
                raise Exception
            else:
                pass
            a_trans_list.extend(train_result)
            success +=1
            get_trans=False
            time.sleep(0.1)
        except:
            pass
    if success%10==0:
        print(success)
        print(a_trans_list[-10:])
    time.sleep(0.1)

assert len(a_list)==len(a_trans_list)
print('翻译顺利结束！')
print(a_trans_list)

