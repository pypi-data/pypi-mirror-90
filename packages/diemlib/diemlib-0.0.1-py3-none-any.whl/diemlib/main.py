#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module documentation goes here
   and here
   and ...
"""

import requests
import time
import json
import os
import datetime
from sys import exit
import diemlib.config as config

__all__ = ["UtcNow", "printl", "mq", "out", "endJob", "endjob", "error"]


def UtcNow():
    now = datetime.datetime.utcnow()
    return now.strftime("%Y-%m-%dT%H:%M:%S") + "Z"


def printl(msg):
    print(msg)


def mq(data):
    data["id"] = config.__id
    data["jobid"] = config.__jobid
    data["transid"] = config.__transid
    data["email"] = config.__email
    data["name"] = config.__name

    try:
        if "out" in data:
            res = data.get("out")
            if not isinstance(res, (int, float, str, bool, dict)):
                data[
                    "out"
                ] = "Response must be booleam, number or string (including json) "

    except Exception as e:
        error(e)
        raise

    requests.post(url=config.__url, data=data)


def out(data):
    mq({"out": data})


def endJob(kwargs):
    try:
        Completed = "Completed"
        Failed = "Failed"
        Stopped = "Stopped"
        failMsg1 = "Missing Status Keyword"
        failMsg2 = "Status Field Should be of String Data Type"
        failMsg3 = "Status Field Not set Properly. Allowed Values are (Completed,Failed,Stopped)"
        failMsg4 = "Out Field Should be of either a String or Object Type"
        failMsg5 = "Count Field Should be of String Data Type"

        coreEndStatus = [Completed, Failed, Stopped]

        failMessage = []
        data = {}

        if len(kwargs) == 0:
            failMessage.append(failMsg1)

        for key, value in kwargs.items():
            if key == "status" and not isinstance(value, str):
                failMessage.append(failMsg2)
                continue
            if key == "status" and value not in coreEndStatus:
                failMessage.append(failMsg3)
                continue
            if key == "out" and not isinstance(value, (str, dict)):
                failMessage.append(failMsg4)
                continue
            if key == "count" and not isinstance(value, int):
                failMessage.append(failMsg5)
                continue
            data[key] = value

        if len(failMessage) > 0:
            data["status"] = Failed
            data["out"] = ". ".join(str(msg) for msg in failMessage)

        data["jobend"] = UtcNow()

        mq(data)

        msg = f"--- job {id} finished at {UtcNow()} --- running time: {time.time() - config.__starttime} ---"

        printl(msg)
        exit()

    except Exception as e:
        data = {"status": Failed, "out": e}
        error(e)


def endjob():
    data = {"status": "Completed", "count": config.__count}
    endJob(data)


def error(err):
    printl(err)
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "email": config.__email,
        "error": str(err),
        "id": config.__id,
        "jobid": config.__jobid,
        "jobend": now,
        "name": config.__name,
        "status": "Failed",
    }
    mq(data)
    msg = f"Job {config.__id} failed - time: {UtcNow()} - runtime: {time.time() - config.__starttime}"
    printl(msg)
    exit(1)