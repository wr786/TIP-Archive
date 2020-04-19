import requests
import re
from bs4 import BeautifulSoup
import time

stuID = "0"
file = open(f"{stuID}_StatData.txt", "w", encoding="utf-8")
base_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}
headers["Accept"]="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"


def dfs(url, prefix_time):
    time.sleep(0.2)
    print(f"[INFO] 当前层级:{prefix_time}; 正在爬取:{url}")
    while True:     # 为了解决访问异常，如果发生异常就再继续一次
        try:
            response = requests.get(url, headers = headers, timeout = 20)    
            break
        except requests.exceptions.ConnectionError:
            print('[ERROR] ConnectionError -- please wait 1 seconds')
            time.sleep(3)
        except requests.exceptions.ChunkedEncodingError:
            print('[ERROR] ChunkedEncodingError -- please wait 1 seconds')
            time.sleep(3)    
        except:
            print('[ERROR] Unfortunitely -- An Unknow Error Happened, Please wait 1 seconds')
            time.sleep(3)
    # response = requests.get(url)
    response.encoding = 'gb2312'
    data = response.text
    data.replace('\ufffd', '')
    # print(response)
    oBS = BeautifulSoup(response.text, "html.parser")
    if len(oBS.find_all("tr", class_="villagetr")):     # 搜索的终点，需要return
        for item in oBS.find_all("tr", class_="villagetr"):
            itm = list(item.children)
            file.write(prefix_time*"\t" + itm[0].string + itm[2].string + itm[1].string + '\n')   # 调整顺序
        return
    if prefix_time == 0:    # 这时是省，需要特殊处理
        items = oBS.find_all("a", class_="")
        for item in items:
            file.write(item['href'][:2] + 10*'0')   # 输出级别
            file.write(item.text + '\n')
            dfs(url[:url.rfind("/")+1] + item['href'], prefix_time+1)
    else:
        items = oBS.find_all("a", class_="")
        # 这时，偶数位对应的是代码，奇数位对应的是名称
        for idx in range(0, len(items), 2):
            file.write(prefix_time*"\t" + items[idx].text)
            file.write(items[idx+1].text + '\n')
            dfs(url[:url.rfind("/")+1] + items[idx]['href'], prefix_time+1)


if __name__ == "__main__":
    startTime = time.time()
    base_affix = "index.html"
    dfs(base_url + base_affix, 0)
    file.close()
    endTime = time.time()
    print(f"[INFO] 爬取在{endTime - startTime}s内完成!")