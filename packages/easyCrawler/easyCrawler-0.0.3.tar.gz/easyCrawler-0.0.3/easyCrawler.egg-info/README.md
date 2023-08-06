### 简易爬虫0.0.3 使用手册   
#### easyCrawler0.0.3 User's guidance
[https://github.com/theCoder-WM]点击此处反馈问题_click_here_to_feedback

```python
from easyCrawler import *

url = '***'
crawler = Crawler(url)
crawler.get_soup()
crawler.find_all('span', class_name='hello-world')
crawler.data_processing()   # data.text
crawler.data_processing('href')   # data.attrs['href']
print(crawler.data_new)
```
