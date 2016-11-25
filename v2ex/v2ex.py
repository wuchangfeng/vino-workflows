#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow, web


ICON_DEFAULT = 'icon.png'


# 加载
def today():
    

    url = 'https://www.v2ex.com/api/topics/hot.json'
    r = web.get(url)
    # throw an error if request failed, Workflow will catch this and show it to the user
    r.raise_for_status()    
    data = r.json()
    
    return data



def main(wf):
    
    # 请求数据
    news = wf.cached_data('today', today, max_age=60)    
    # 添加 item 到 workflow 列表
    for new in news:

        wf.add_item(title=new['title'],
                    subtitle=new['content'],
                    arg=new['url'],
                    valid=True,
                    icon=ICON_DEFAULT)
   
    
    wf.send_feedback()
    


if __name__ == '__main__':
    
    wf = Workflow()

    logger = wf.logger

    sys.exit(wf.run(main))

  

