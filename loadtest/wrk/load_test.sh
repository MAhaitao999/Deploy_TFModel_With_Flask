wrk -c 8 -d 20s --timeout=20s -s file.lua http://127.0.0.1:5000/stream_predict
wrk -c 8 -d 20s --timeout=20s -s file.lua http://127.0.0.1:5000/predict