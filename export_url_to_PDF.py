"""
# 说明：此脚本用于将页面导出为PDF
# Date: None
# 依赖：PhantomJS，Python的selenium库
# 用法：使用时传入一个URL或者文本文件名(其中每行为一个URL)，将把它们导出为PDF文件
        => python3 导出页面为PDF.py "https://www.baidu.com"
        => python3 导出页面为PDF.py urls.txt

# 备注：1.使用前请先设置"PhantomJS_PATH"为PhantomJS执行文件路径
        2.如果导出的页面加载不完全，请增大"TIME_INTERVAL"变量的数值
"""
import re
from sys import argv
from os.path import exists

from magic import print_spend_time

from selenium import webdriver


PhantomJS_PATH = "/home/fa/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"  # PhantomJS执行文件路径
TIME_INTERVAL = 500  # 滚动页面的时间间隔，单位为ms
SCROLLING_PAGE_SCRIPT = """
    (function() {
        var y = 0;
        var step = 100;
        window.scroll(0, 0);

        function f() {
            if (y < document.body.scrollHeight) {
                y += step;
                window.scroll(0, y);
                setTimeout(f, 500);  // 如果导出的页面加载不完全，请自行加大这里的数值
            } else {
                window.scroll(0, 0);
                document.title += "scroll-done";
            }
        } 
        setTimeout(f, 1000);
    })()
"""

browser = webdriver.PhantomJS(executable_path=PhantomJS_PATH)
browser.command_executor._commands['executePhantomScript'] = (
    'POST', '/session/$sessionId/phantom/execute')


def save_to_pdf(url):
    """输入网址，保存页面为PDF"""
    try:
        browser.get(url)
        print("导出：", browser.title, ".pdf", end="")
        browser.execute_script(SCROLLING_PAGE_SCRIPT)
        while not "scroll-done" in browser.title:
            pass
        # 规范页面格式
        pageformat = 'this.paperSize = {format: "A4", orientation: "portrait" };'
        browser.execute('executePhantomScript', {
                        'script': pageformat, 'args': []})
        filename = browser.title.replace("scroll-done", "")
        filename = re.sub(r"[ /\-\?:\|]+", "_", filename)
        render_script = 'this.render("%s.pdf")' % filename
        browser.execute('executePhantomScript', {'script': render_script, 'args': []})

        return True
    except Exception as err:
        print("[!]", err)
        return False


@print_spend_time("，共耗时：{h}时{m}分{s}秒。")
def main():
    """主程序"""
    script, input_text = argv
    urls_list = []
    success_count = 0

    if input_text.startswith("http"):
        urls_list.append(input_text)
    
    elif exists(input_text):
        with open(input_text, 'r') as f:
            urls = f.read().splitlines()
            urls_list.extend(urls)
    else:
        print("输入格式错误或文件不存在！")
        exit(1)
    
    print("处理中...")
    for url in urls_list:
        if url.startswith("http"):
            if save_to_pdf(url):
                print("\033[94m", "--成功", "\033[0m")
                success_count += 1
            else:
                print("\033[31m", "--失败", "\033[0m")
    
    print("处理完成，成功%d个，失败%d个" % \
            (success_count, len(urls_list)-success_count), end="")


if __name__ == "__main__":
    main()
