#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import redis


class RedisPool:
    def __init__(self):
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379)

    def get_conn(self):
        return self.pool
