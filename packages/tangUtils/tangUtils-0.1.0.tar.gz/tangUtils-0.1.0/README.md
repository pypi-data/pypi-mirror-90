# tangUtils
根据个人使用习惯, 将一些 文件、目录、命令行交互 相关操作做了一个语法糖

## examples
``` python
from tangUtils.main import File
from tangUtils.mail import Mail

root = File(__file__).parent

em = Mail(fromAddr=("王小明", "10086@qq.com"), password="your auth code")
toAddr = [
  "10000@qq.com",
  ("王钢蛋", "10010@qq.com"),
]
subject = "来自王小明的提醒"
fallbackText="您的客户端无法显示此类型的消息(html), 请换用其它客户端以查看该超文本内容"
html="""
  <!DOCTYPE html>
  <html lang="zh-cn">
  <body>
    <div>您已接收到来自<strong>王小明</strong>的提示</div>
    <!-- 邮箱客户端一般会屏蔽不同域的图片链接, 可以将图片放到附件中 -->
    <!-- src 使用 cid:idx, idx 是图片所在的文件序号 -->
    <img src="cid:1" alt="picture">
  </body>
  </html>
"""
em.sendTo(toAddr=toAddr, subject=subject, fallbackText=fallbackText, html=html, attachment=root.files)
em.quit()
```
