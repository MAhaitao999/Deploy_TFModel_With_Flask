# Deploy_TFModel_With_Flask

deploy your TensorFlow model with Flask

### 说明

为方便测试, 我把请求图片解析的部分省略掉了, 直接用Get请求的方式, 把img作为全局变量传进去.

压测工具选取的是ab-test, 启动命令如下:

```sh
ab -n 1000 -c 100 127.0.0.1:5000/predict
```

### 测试环境

- CPU: Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz
- 内存: 16G
- GPU: None

### 不同部署形式的性能比较(ms)
部署形式 | 50% | 66% | 75% | 80% | 90% | 95% | 98% | 99% | 100% | rps(#/s)
---|---|---|---|---|---|---|---|---|---|---
threaded=False, processes=1 | 4631 | 4649 | 4661 | 4670 | 4689 | 4694 | 4700 | 4703 | 4854 | 21.47
threaded=True, processes=1 | 389 | 540 | 705 | 2095 | 16671 | 23675 | 26182 | 26387 | 26536 | 27.08
gunicorn -w 8 -b 127.0.0.1:5000 main:app | 3596 | 3784 | 3903 | 3950 | 4018 | 4065 | 4111 | 4163 | 4311 | 26.68
threaded=False, processes=8 | 直接锁死, 没法做推理, 具体原因可参见[issue](https://github.com/tensorflow/tensorflow/issues/5448)
