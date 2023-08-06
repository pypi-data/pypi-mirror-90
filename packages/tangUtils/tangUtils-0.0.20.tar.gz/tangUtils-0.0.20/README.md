# tangUtils
根据个人使用习惯, 将一些 文件、目录、命令行交互 相关操作做了一个语法糖

## examples
``` python
from tangUtils.main import File

tempPath = __file__

for f in File(tempPath).parent.asDir().files:
  print(f.name, f.suffix)
```
