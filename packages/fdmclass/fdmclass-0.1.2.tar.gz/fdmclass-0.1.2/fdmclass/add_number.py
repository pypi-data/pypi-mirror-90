#coding=utf-8
import sys
import json

from fdmutils.common     import get_tb_info
from fdmutils.common     import show_dict_intree
from fdmutils.data_var   import my_linf    ## 负无穷
from fdmutils.data_var   import my_rinf    ## 正无穷

class CAddNumberObj():
    def __init__(self,_debug=False):
        self.debug = _debug
        pass

    def add(self,a,b):
        """
        @note   : 加法运算
        @param a: 数值型变量
        @param b: 数值型变量
        @return dst: 结果
        """
        msg     = "success"
        flag    = 0
        dst     = 0

        try:
            dst  = a+b
        except:
            msg  = get_tb_info()
            flag = -1
            dst  = None
        return msg,flag,dst




if __name__ == "__main__":
    print("call CAddNumberObj")
    sys.exit(0)
