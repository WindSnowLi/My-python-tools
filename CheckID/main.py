import json
from datetime import datetime
from locale import NOEXPR

# 所有的区域编码表
idMap = json.load(open('./id.json', 'r', encoding='utf8'))

# 当前时间
current_date = datetime.now().date()


def isID(digs):
    if len(digs) != 17 or digs.isdigit() == False:
        raise ValueError('长度错误或不是数字:%s' % digs)
    if digs[:6] not in idMap:
        raise Exception('区号异常，或是已弃用不在表中：%s' % digs[:6])

    birthday = None
    try:
        birthday = datetime.strptime(digs[6:14], "%Y%m%d").date()
        if birthday > current_date:
            raise ValueError('出生年月异常：%s' % digs[6:14])
    except Exception as e:
        raise ValueError('出生年月异常：%s' % digs[6:14])

    return ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'][sum(
        [int(digs[i]) * [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2][i] for i in range(17)]) % 11]


if __name__ == "__main__":
    # 可自行封装数据来源
    example = ['110115195708043734',
               '100115195708043734',  # 区号错误
               '210203197503102721',
               '210203197503102720',  # 校验位错误
               '520323197806058856',
               '520323197806508856'   # 出生日期错误
               ]
    for i in example:
        try:
            if i[len(i)-1] != isID(i[:-1]):
                print('校验位错误:%s' % i)
        except ValueError as e:
            print(e.args)
        except Exception as e:
            print(e)
