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

All the results are tested with ApacheBench.

```sh
ab -n 100 -c 24 -T 'application/json' -H "accept: application/json" -p dog_req.json $url
```

|| 50% | 66% | 75% | 80% | 90% | 95% | 98% | 99% | 100% | rps(#/s)
---|---|---|---|---|---|---|---|---|---|---
threaded=False, processes=1 | 4994 | 5000 | 5012 | 5055 | 5067 | 5073 | 5075 | 5075 | 5075 | 4.79
threaded=True, processes=1 | 4207 | 4380 | 4521 | 4679 | 6212 | 6288 | 7109 | 7132 | 7132 | 5.42
gunicorn -w 8 -b 127.0.0.1:5000 main:app | 1605 | 1627 | 1657 | 1662 | 1712 | 1745 | 1793 | 1882 | 1882 | 14.66
main_service_streamer_locust.py batch_size = 2| 4684 | 4709 | 4732 | 4756 | 4761 | 4763 | 4766 | 4766 | 4766 | 5.10
main_service_streamer_locust.py batch_size = 4| 4720 | 4742 | 4780 | 4785 | 4791 | 4873 | 4898 | 4898 | 4898 | 5.04
main_service_streamer_locust.py batch_size = 8| 4767 | 4841 | 4860 | 4917 | 4964 | 5091 | 5309 | 5369 | 5369 | 4.98
main_service_streamer_locust.py batch_size = 16| 4816 | 4883 | 4913 | 4920 | 5001 | 5181 | 5905 | 6333 | 6333 | 4.97


### Tips:

When you deploy with `threaded=False, processes=8`, The server is locked, and cannot do inference. If you want to known the reason please refer to the [issue](https://github.com/tensorflow/tensorflow/issues/5448)
