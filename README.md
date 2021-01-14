# Deploy_TFModel_With_Flask

deploy your TensorFlow model with Flask

### Description

- If you just want to test whether the service work properly, you can use only one client to send a request. For details, please refer to `loadtest/single_client` directory;

- ApacheBench Test: `sudo apt-get install apache2-utils`, please refer to `loadtest/ApacheBench` directory;

- Locust: `pip install locustio==0.11.0`, please refer to `loadtest/Locust` directory;

- wrk: A very good pressure testing tool, but need to use Lua language, I don't know how to use Lua language to Base64 encode pictures(if you know please tell me in the issue). If you want to try the wrk, please start the service through the command `python3 main_ service_ streamer_ wrk.py` and refer to the `loadtest/wrk` directory for testing.

```
sudo apt-get install libssl-dev
git clone https://github.com/wg/wrk.git
cd wrk
make 
```

### Test environment

- CPU: Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz　8 core
- RAM: 16G
- GPU: None

### Performance comparison of different deployment(ms)
| 50% | 66% | 75% | 80% | 90% | 95% | 98% | 99% | 100% | rps(#/s)
---|---|---|---|---|---|---|---|---|---|---
threaded=False, processes=1 | 4631 | 4649 | 4661 | 4670 | 4689 | 4694 | 4700 | 4703 | 4854 | 21.47
threaded=True, processes=1 | 389 | 540 | 705 | 2095 | 16671 | 23675 | 26182 | 26387 | 26536 | 27.08
gunicorn -w 8 -b 127.0.0.1:5000 main:app | 3596 | 3784 | 3903 | 3950 | 4018 | 4065 | 4111 | 4163 | 4311 | 26.68


### Tips:

When you deploy with `threaded=False, processes=8`, The server is locked, and cannot do inference. If you want to known the reason please refer to the [issue](https://github.com/tensorflow/tensorflow/issues/5448)
