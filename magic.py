"""
# Python实用函数

# 包含函数：
print_with_style()     ----- 拓展print()函数，使其输出时可以携带样式
print_spend_time()装饰器  ----- 获取某函数执行时所消耗的时间
"""
from functools import wraps
from datetime import datetime


def print_with_style(*args, style='', **kwargs):
    """带样式的打印，它是对print()函数的拓展.

    # 参数：
        style:要使用的样式，它可以是以下值：(多个样式之间用加号'+'隔开)
                    'r'：红色
                    'g'：绿色
                    'b'：蓝色
                    'B'：加粗
                    'U'：下划线
                    其它： 其它格式控制代码，如：'\033[7m'
        others：指其它可用于print()函数的参数，如end, sep, file等.
    # 例子：
        print_with_style(value, ..., style='g+B')
        print_with_style(value, ..., style='B+\033[7m', sep='>')
    """
    styles = {
        'r': '\033[31m',  # 红色
        'g': '\033[92m',  # 绿色
        'b': '\033[94m',  # 蓝色
        'B': '\033[1m',  # 加粗
        'U': '\033[4m'  # 下划线
    }

    style_lsit = set(style.split('+'))
    for s in style_lsit:
        if s in styles:
            print(styles[s], end='')
        elif s.startswith('\033'):
            print(s, end='')

    print(*args, **kwargs)
    print('\033[0m', end='')


def print_spend_time(format_str='执行函数{func_name}，共耗时：{d}天{h}小时{m}分钟{s:02d}秒{ms}微秒', end='\n'):
    """获取函数执行时间的装饰器，可对输出字符串进行定制.
    
    # 参数：
        format_str: 定制的输出字符串，可在其中使用的插槽有：
                    {d}: 天,
                    {h}：小时,
                    {m}：分钟,
                    {s}：秒,
                    {ms}：微秒,
                    {th}：总小时,
                    {tm}：总分钟,
                    {ts}：总秒,
                    {tms}：带微秒的总秒,
                    {func_name}：执行的函数名
        end: 换行符，默认为'\\n'
    # 例子：
        @print_spend_time(format_str='执行完成，共耗时：{tms} s')
        def f():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = func(*args, **kwargs)  # 执行被包装的函数
            end_time = datetime.now()
            spend_time = end_time - start_time

            m, s = divmod(spend_time.seconds, 60)  # seconds
            h, m = divmod(m, 60)  # hours, minutes
            d = spend_time.days  # days
            ms = spend_time.microseconds  # microseconds
            th = d*24 + h  # total hours
            tm = d*24*60 + h*60 + m  # total minutes
            ts = d*24*60*60 + spend_time.seconds  # total seconds
            tms = ts + spend_time.microseconds  # total seconds with microseconds
            
            final_str = format_str.format(d=d, h=h,
                                          m=m, s=s,
                                          ms=ms, th=th,
                                          tm=tm, ts=ts,
                                          tms=tms,
                                          func_name=func.__name__ + '()')
            print(final_str, end=end)
            
            return result
        return wrapper
    return decorator
