"""
# 用于生成日历markdown文件的小程序
# Date:2017-9-3
"""

from datetime import datetime
from calendar import monthrange


def get_list(xq, count):
    """填充日期，生成一个按星期排布的列表"""
    list = [['','','','','','',''],
            ['','','','','','',''],
            ['','','','','','',''],
            ['','','','','','',''],
            ['','','','','','',''],
            ['','','','','','','']
           ]
    n = 0
    day = 1
    for row in list:
        for col in row:
            if n >= xq and n <= 42:
                if n < 7:
                    list[n//7][n] = day
                else:
                    list[n//7][n%7] = day
                day = day + 1
            if day == count + 1:
                if list[-1][0] == '':
                    list = list[:-1]
                if xq == 7:
                    list = list[1:]
                return list
            n = n + 1


def create_one(year, month):
    """生成给定年月的MD日历文件"""
    dt = datetime(year, month, 1)
    xq = int(dt.strftime('%u'))  # 该月的1号是星期几
    count = monthrange(year, month)[1]  # 该月一共有多少天
    
    list = get_list(xq, count)
    # 开始写文件
    with open('%d年%d月.md' % (year,month), 'w') as f:
        f.write('# %d年%d月' % (year,month) + '\n')
        f.write('|日|一|二|三|四|五|六|' + '\n')
        f.write('|:-|:-|:-|:-|:-|:-|:-|' + '\n')
        
        r = 0
        for row in list:
            string = ''
            c = 0
            for col in row:
                num = list[r][c]
                if num == '':
                    string += '|'
                else:
                    string += '|**%d** ' % num
                c = c + 1
            string += '|'
            f.write(string + '\n')
            r = r + 1


if __name__ == '__main__':
    for month in range(1,13):
        create_one(2017, month)

