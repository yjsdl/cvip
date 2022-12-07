# -*- coding: utf-8 -*-
# @Time    : 2021/12/15 17:23
# @Author  : ZhaoXiangPeng
# @File    : jiemi1.py


def _TS(_ou: str):
    # _$TS 解密函数
    _Jc = _ou.__len__()
    _oE, _7m, _ME = None, [None] * (_Jc-1), ord(_ou[0]) - 97
    _uw = 0
    for _ in range(1, _Jc):
        _oE = ord(_ou[_])
        if (_oE >= 40) & (_oE < 92):
            _oE += _ME
            if _oE > 92:
                _oE = _oE - 52
        elif (_oE >= 97) & (_oE < 127):
            _oE += _ME
            if _oE >= 127:
                _oE = _oE - 30
        _7m[_uw] = _oE
        _uw += 1
    print(_7m)
    result = ''.join([chr(i) for i in _7m])
    return result


if __name__ == '__main__':
    print(_TS("n%yr~~veyvru%S%gvfg6rwv6bev%S%gvfg6rwv7ezive%S%gvfg6rwv<wer~v7ezive%S%gvfg6rwv4hgb~rgzba%"))
