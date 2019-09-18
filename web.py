# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 11:31:30 2019

@author: gyae
"""

import socket

socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_1.connect(("localhost", 5555)) # Address tuple

socket_1.send(bytes("hello world", encoding="UTF-8"))