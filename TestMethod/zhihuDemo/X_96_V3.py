import struct
import requests
import time,re
import json
import jsonpath
import hashlib
import urllib.parse   #is_end=true  获取完  false没获取完
import execjs
import ctypes
import binascii
from _md5 import md5
from lxml import etree
class x_zse_96_V3(object):
    local_48 = [48, 53, 57, 48, 53, 51, 102, 55, 100, 49, 53, 101, 48, 49, 100, 55]
    local_55 = "6fpLRqJO8M/c3jnYxFkUVC4ZIG12SiH=5v0mXDazWBTsuw7QetbKdoPyAl+hN9rgE"
    h = {
        "zk": [1170614578, 1024848638, 1413669199, -343334464, -766094290, -1373058082, -143119608, -297228157, 1933479194, -971186181, -406453910, 460404854, -547427574, -1891326262, -1679095901, 2119585428, -2029270069, 2035090028, -1521520070, -5587175, -77751101, -2094365853, -1243052806, 1579901135, 1321810770, 456816404, -1391643889, -229302305, 330002838, -788960546, 363569021, -1947871109],
        "zb": [20, 223, 245, 7, 248, 2, 194, 209, 87, 6, 227, 253, 240, 128, 222, 91, 237, 9, 125, 157, 230, 93, 252, 205, 90, 79, 144, 199, 159, 197, 186, 167, 39, 37, 156, 198, 38, 42, 43, 168, 217, 153, 15, 103, 80, 189, 71, 191, 97, 84, 247, 95, 36, 69, 14, 35, 12, 171, 28, 114, 178, 148, 86, 182, 32, 83, 158, 109, 22, 255, 94, 238, 151, 85, 77, 124, 254, 18, 4, 26, 123, 176, 232, 193, 131, 172, 143, 142, 150, 30, 10, 146, 162, 62, 224, 218, 196, 229, 1, 192, 213, 27, 110, 56, 231, 180, 138, 107, 242, 187, 54, 120, 19, 44, 117, 228, 215, 203, 53, 239, 251, 127, 81, 11, 133, 96, 204, 132, 41, 115, 73, 55, 249, 147, 102, 48, 122, 145, 106, 118, 74, 190, 29, 16, 174, 5, 177, 129, 63, 113, 99, 31, 161, 76, 246, 34, 211, 13, 60, 68, 207, 160, 65, 111, 82, 165, 67, 169, 225, 57, 112, 244, 155, 51, 236, 200, 233, 58, 61, 47, 100, 137, 185, 64, 17, 70, 234, 163, 219, 108, 170, 166, 59, 149, 52, 105, 24, 212, 78, 173, 45, 0, 116, 226, 119, 136, 206, 135, 175, 195, 25, 92, 121, 208, 126, 139, 3, 75, 141, 21, 130, 98, 241, 40, 154, 66, 184, 49, 181, 46, 243, 88, 101, 183, 8, 23, 72, 188, 104, 179, 210, 134, 250, 201, 164, 89, 216, 202, 220, 50, 221, 152, 140, 33, 235, 214],
        "zm": [120, 50, 98, 101, 99, 98, 119, 100, 103, 107, 99, 119, 97, 99, 110, 111]
    }

    @staticmethod
    def pad(data_to_pad):
        padding_len = 16 - len(data_to_pad) % 16
        padding = chr(padding_len).encode() * padding_len
        return data_to_pad + padding

    @staticmethod
    def unpad(padded_data):
        padding_len = padded_data[-1]
        return padded_data[:-padding_len]

    @staticmethod
    def left_shift(x, y):
        x, y = ctypes.c_int32(x).value, y % 32
        return ctypes.c_int32(x << y).value

    @staticmethod
    def Unsigned_right_shift(x, y):
        x, y = ctypes.c_uint32(x).value, y % 32
        return ctypes.c_uint32(x >> y).value

    @classmethod
    def Q(cls, e, t):
        return cls.left_shift((4294967295 & e), t) | cls.Unsigned_right_shift(e, 32 - t)

    @classmethod
    def G(cls, e):
        t = list(struct.pack(">i", e))
        n = [cls.h['zb'][255 & t[0]], cls.h['zb'][255 & t[1]], cls.h['zb'][255 & t[2]], cls.h['zb'][255 & t[3]]]
        r = struct.unpack(">i", bytes(n))[0]
        return r ^ cls.Q(r, 2) ^ cls.Q(r, 10) ^ cls.Q(r, 18) ^ cls.Q(r, 24)

    @classmethod
    def g_r(cls, e):
        n = list(struct.unpack(">iiii", bytes(e)))
        [n.append(n[r] ^ cls.G(n[r + 1] ^ n[r + 2] ^ n[r + 3] ^ cls.h['zk'][r])) for r in range(32)]
        return list(struct.pack(">i", n[35]) + struct.pack(">i", n[34]) + struct.pack(">i", n[33]) + struct.pack(">i", n[32]))

    @classmethod
    def re_g_r(cls, e):
        n = [0] * 32 + list(struct.unpack(">iiii", bytes(e)))[::-1]
        for r in range(31, -1, -1):
            n[r] = cls.G(n[r + 1] ^ n[r + 2] ^ n[r + 3] ^ cls.h['zk'][r]) ^ n[r + 4]
        return list(struct.pack(">i", n[0]) + struct.pack(">i", n[1]) + struct.pack(">i", n[2]) + struct.pack(">i", n[3]))

    @classmethod
    def g_x(cls, e, t):
        n = []
        i = 0
        for _ in range(len(e), 0, -16):
            o = e[16 * i: 16 * (i + 1)]
            a = [o[c] ^ t[c] for c in range(16)]
            t = cls.g_r(a)
            n += t
            i += 1
        return n

    @classmethod
    def re_g_x(cls, e, t):
        n = []
        i = 0
        for _ in range(len(e), 0, -16):
            o = e[16 * i: 16 * (i + 1)]
            a = cls.re_g_r(o)
            t = [a[c] ^ t[c] for c in range(16)]
            n += t
            t = o
            i += 1
        return n

    @classmethod
    def b64encode(cls, md5_bytes: bytes, device: int = 0, seed: int = 63) -> str:
        local_50 = bytes([seed, device]) + md5_bytes  # 随机数  0 是环境检测通过
        local_50 = cls.pad(bytes(local_50))
        local_34 = local_50[:16]
        local_35 = [local_34[local_11] ^ cls.local_48[local_11] ^ 42 for local_11 in range(16)]
        local_36 = cls.g_r(local_35)
        local_38 = local_50[16:]
        local_39 = cls.g_x(local_38, local_36)
        local_53 = local_36 + local_39
        local_56 = 0
        local_57 = ""
        for local_13 in range(len(local_53) - 1, 0, -3):
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_59 = local_53[local_13] ^ cls.Unsigned_right_shift(58, local_58) & 255
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_59 = local_59 | (local_53[local_13 - 1] ^ cls.Unsigned_right_shift(58, local_58) & 255) << 8
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_59 = local_59 | (local_53[local_13 - 2] ^ cls.Unsigned_right_shift(58, local_58) & 255) << 16
            local_57 = local_57 + cls.local_55[local_59 & 63]
            local_57 = local_57 + cls.local_55[cls.Unsigned_right_shift(local_59, 6) & 63]
            local_57 = local_57 + cls.local_55[cls.Unsigned_right_shift(local_59, 12) & 63]
            local_57 = local_57 + cls.local_55[cls.Unsigned_right_shift(local_59, 18) & 63]
        return local_57

    @classmethod
    def b64decode(cls, x_zse_96: str) -> dict:
        local_56 = 0
        local_57 = []
        for local_13 in range(0, len(x_zse_96), 4):
            local_59 = (cls.local_55.index(x_zse_96[local_13 + 3]) << 18) + (cls.local_55.index(x_zse_96[local_13 + 2]) << 12) + (cls.local_55.index(x_zse_96[local_13 + 1]) << 6) + cls.local_55.index(x_zse_96[local_13])
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_57.append((local_59 & 255) ^ cls.Unsigned_right_shift(58, local_58))
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_57.append(((local_59 >> 8) & 255) ^ cls.Unsigned_right_shift(58, local_58))
            local_58 = 8 * (local_56 % 4)
            local_56 = local_56 + 1
            local_57.append(((local_59 >> 16) & 255) ^ cls.Unsigned_right_shift(58, local_58))
        local_36, local_39 = local_57[-16:][::-1], local_57[:-16][::-1]
        local_38 = cls.re_g_x(local_39, local_36)
        local_35 = cls.re_g_r(local_36)
        local_34 = [local_35[local_11] ^ cls.local_48[local_11] ^ 42 for local_11 in range(16)]
        local_50 = cls.unpad(bytes(local_34 + local_38))
        return {
            'seed': local_50[0],
            'device': local_50[1],
            'md5_bytes': local_50[2:]
        }
