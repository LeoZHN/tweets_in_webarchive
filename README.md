# Twitter Scraper （Tweets in WebArchive） 使用说明

尚在编辑中，请勿使用。

这是一个简单的Twitter历史数据爬虫工具。它借助Web Archive上关于Twitter的历史网页快照，可以帮助您获取特定时间段内的Twitter推文。

基于Gitee项目：https://gitee.com/wojiaoyishang/get-tweets 开发，使用Playwright和Python。

本工具依照2016年的Twitter网页HTML结构遍历网页快照，寻找特定时间段内的推文并截取内容，可能不适用于其他时间段的网页快照。

## 使用步骤

1. 解压下载的压缩文件。

2. 双击运行 `run_scraper.bat` 文件。

3. 程序将自动开始运行，您会看到一个命令行窗口显示爬取进度。

4. 爬取完成后，结果将保存在同一文件夹下的 `tweets.txt` 文件中。

5. 查看 `tweets.txt` 文件以获取爬取的推文内容。

注意：首次运行可能需要一些时间来设置环境。请耐心等待，不要关闭任何弹出的窗口。

如果您需要修改爬取的设置（如日期范围或目标URL），请修改`config.json`中的对应参数。支持修改爬取开始和结束日期，以及爬取URL。

祝使用愉快！
