#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow, web
import datetime

ICON_DEFAULT = 'icon.png'


# 加载今天的干货列表
def today():
    
    now = datetime.datetime.now()
   
    url = 'http://gank.io/api/day/' + now.strftime("%Y/%m/%d")
    
    r = web.get(url)

    # throw an error if request failed, Workflow will catch this and show it to the user
    r.raise_for_status()

    ganks = []
    data = r.json()
    
    # 解析数据
    results = data['results']
    # 测试数据
    #print(results)
    categories = data['category']
    results = data['results']
    for category in categories:
        for gank in results[category]:
            ganks.append(gank)

    return ganks



def main(wf):
    
    # 请求数据
    ganks = wf.cached_data('today', today, max_age=60)
    
    if len(ganks) <= 0:
            wf.add_item(title=u'今天还没发干货', valid=True, icon=ICON_DEFAULT)

    
    # 添加 item 到 workflow 列表
    for gank in ganks:

        sub =  gank['type'] 
        wf.add_item(title=gank['desc'],
                    subtitle=sub,
                    arg=gank['url'],
                    valid=True,
                    icon=ICON_DEFAULT)
   
    
    wf.send_feedback()
    


if __name__ == '__main__':
    
    wf = Workflow()

    logger = wf.logger

    sys.exit(wf.run(main))

  

