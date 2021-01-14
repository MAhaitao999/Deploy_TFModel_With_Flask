# !/usr/bin/env bash
# -*- coding: utf-8 -*-

if [[ $#<=0 ]]; then
	echo "command=>$0, no parameters"
    echo "please input stream_predict or predict"
	exit 1
fi
 
ip="http://127.0.0.1:5000/"
url=$ip$@

echo "=============request: "$url
ab -n 100 -c 24 -T 'application/json' -H "accept: application/json" -p dog_req.json $url
