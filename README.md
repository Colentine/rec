### 安装环境(python3.10)
```
- pip install -r requirements.txt
```

### 执行命令
```
   python main.py -m -a -b
```
  - -m 模型名称，例如gpt-4o
  - -a 输入api key
  - -b 输入base url

### 结果会保存在result.json
每个模型100个测试   
结果样例：
```json
{  
  "gpt-4o":{  
        "hit5": 0.8133333333333334,  
        "hit3": 0.6733333333333333,  
        "hit1": 0.49333333333333335,
        "error_rate": 0.01,
        "avg_pos": 2.54
  },
  "qwen-plus": {  
        "hit5": 0.7633333333333333,  
        "hit3": 0.65,  
        "hit1": 0.44333333333333336,  
        "error_rate": 0.0,  
        "avg_pos": 3.3   
  }   
}
```

* hit5: Ground Truth 出现在前五(包括五)的概率  
* hit3: Ground Truth 出现在前三(包括三)的概率  
* hit1: Ground Truth 出现在第一的概率   
* error_rate: 模型输出错误格式的概率   
* avg_pos: Ground Truth在模型输出排序里的平均位置# rec
