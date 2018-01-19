# 自动化测试框架使用说明

该框架主要使用selenium进行web的自动化测试，但不仅仅限制于UI的自动化测试，请保持与aicp的ui自动化测试联合使用，可达到最佳的效果。


# 使用说明

## 安装部署
```
//进行测试
python setup.py test
//安装到库里
python setup.py install
//生成安装包到dist目录下
python setup.py sdist
```

## 驱动driver的安装

需要下载相关的driver放到系统path路径下
Chrome:     https://sites.google.com/a/chromium.org/chromedriver/downloads
Edge:       https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Firefox:	https://github.com/mozilla/geckodriver/releases
Safari:     https://webkit.org/blog/6900/webdriver-support-in-safari-10/
IE:         http://selenium-release.storage.googleapis.com/index.html

# 主要功能
## 数据和脚本分离
## GUI和脚本分离
## 日志记录分离
## 控件（GUI）自动上传
## 组件（function）自动上传
## 测试用例（case）自动上传
## 测试案例编写
browser关联，日志，场景恢复，数据
## GUI
iframe gui文件 window

## TODO
1. iframe 穿透
2. config文件读取
3. gui文件
4. 等待
5. runner/data
6. fireEvent
