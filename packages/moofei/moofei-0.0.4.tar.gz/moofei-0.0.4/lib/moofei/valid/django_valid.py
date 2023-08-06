#!/usr/bin/python
# -*- coding: UTF-8 -*-
# editor: moofei
'''
by 牧飞 _ __ ___   ___   ___  / _| ___(_)
| '_ ` _ \ / _ \ / _ \| |_ / _ \ |
| | | | | | (_) | (_) |  _|  __/ |
|_| |_| |_|\___/ \___/|_|  \___|_|
'''
__all__ = ['valid', 
           ]

import re
#import sys; sys.path.append('..') #
try:
    from .. import _valid
    from .._valid import  ValidDict, ValidMethod, getFuncDefaults, ValidResultParse
except (ImportError,ValueError):
    from moofei import _valid
    from moofei._valid import  ValidDict, ValidMethod, getFuncDefaults, ValidResultParse
import time
import json
import traceback


class VALID(_valid.VALID):
    @classmethod
    def error(cls, func_name, regula, value, result=None):
        if isinstance(result, dict) and result.get('error'): 
            pass
        else:
            if 0 and func_name:
                message = "Invalid params. Checked (valid) '%s' in the '%s' function, so the value should not be '%s'"%(regula, func_name, value or 'null')
            else:
                message = "Invalid params. Checked (valid) '%s' should  not be '%s'"%(regula, value or 'null')
            result = {'error':{
                        'code':-32602,
                        'message': message
                        }
                     }
        return result     
    
    
def dict_django_update(d, *args):
    for arg in args:
        for k, v in arg.items():
            if isinstance(v, (list,tuple)) and len(v)==1:
                d[k] = v[0] 
            else:
                d[k] = v
    return d                
        
    
class valid:
    @classmethod
    def add(cls, name):
        """valid.add
           >>> @valid.add('beter')
           ... def better(s): return 1,s
           >>> valid.dict(['a:beter'], dict(a="ddddddddddd")) 
        """
        def wrap(fn):
            VALID.addCheck(fn, name=name)
            return fn
        return wrap
        
    @classmethod
    def addCheck(cls, fn, name=None):
        """valid.addCheck
           >>> def better(s): return 1,s
           >>> valid.addCheck(better, 'beter') and None
           >>> valid.dict(['a:beter'], dict(a="ddddddddddd")) 
        """
        VALID.addCheck(fn, name=name)
        return cls
    
    @staticmethod
    def dict(validArgs, awgs):
        '''valid.dict
        >>> valid.dict(['a:int', 'b:true', 'c:ip', r'f:^\d+$'], dict(a=44, b='sss', c='127.0.0.1', f='9ddd9'))
        ('f', '^\\\\d+$')
        '''
        return ValidDict(validArgs, awgs, validCls=VALID)
    
    @staticmethod
    def kDict(validArg, *args, **awgs):
        """valid.kDict
        >>> var_keys = ["var_title", "var_code", "var_memo", "var_content", "upd_can:int", "nid:int"]
        >>> valid.kDict(var_keys, {"upd_can":"0"})
        {'upd_can': 0}
        """
        rs = ValidResultParse(validArg, args, validCls=VALID, **awgs)
        return rs
        
    @staticmethod
    def kDictReal(validArg, *args, **awgs):
        """
           isNotTrue=0, isStrict=0, pops=[]
           >>> var_keys = ["var_title", "var_code", "var_memo", "var_content", "upd_can:int;true", "nid:int"]
           >>> valid.kDictReal(var_keys, {"upd_can":"0"})
           {'upd_can': 0}
        """
        rs = ValidResultParse(validArg, args, validCls=VALID, isNotTrue=1, **awgs)
        return rs

    
    @staticmethod
    def func(validArgs, permit='', rate=None, block=False):
        '''valid.func
        >>> @valid.func(['a:int', 'b:true', 'c:ip', r'f:^\d+$'])
        ... def A(a,b,c,d=3,e=5, f='', **m): pass
        >>> A('3', 'ee', '1.1.1.1',f='64')
        >>> A.validArgs
        ['a:int', 'b:true', 'c:ip', 'f:^\\\\d+$']
        '''
        return ValidMethod(validArgs, validCls=VALID, permit=permit, rate=rate, block=block)

    
    
    @staticmethod
    def doc(cls, allow_api):
        #header("Content-type: text/html;charset=utf-8");
        rs = []
        for api in allow_api:
            fn = getattr(cls, api)
            docs = (fn.func_doc or '').replace('\n', '\n<br>').split('\n', 1)
            doc = docs[1].strip() if len(docs)>1 else None
            validArgs =  getattr(fn, "validArgs", None) or []
            d = {'valid':validArgs,  'doc':doc, 'name':docs[0].strip(), 'api':api}
            rs.append(d)
        return rs
    
    @staticmethod
    def request(fn,  rq, **awgs):
        '''request
        >>> @valid.func(['token:', 'request:','a:int', 'c:code'])
        ... def index_func(token, request, a, c="", **awgs):
        ...     print(token, request, a, c)
        ...     return {'result':{'token':token, 'a':a, 'c':c, 'awgs':awgs}}    
        >>> def index(request):
        ...     return JsonResponse(valid.request(index_func, request))
        '''
        attrs =  getattr(fn, "validArgs", None) or [] #attrs=fn.validArgs
        if attrs:
            dft,keys,argext = fn.func_dft
            isAwgs = 1 if "awgs" in argext else 0
        args = []
        keysL = []
        #d = rq.values
        if rq.is_ajax() and rq.content_type=='application/json':
            form = json.loads(request.read())
        else:
            form = rq.POST
        d = dict_django_update({}, rq.GET, form, rq.FILES)
        
        for attr in attrs:
            param = attr.split(':')[0]
            keysL.append(param)
            if param in awgs: pass #val = awgs.pop(param) 
            else: 
                val = d.get(param, '') #val = rq.form.get(param, '')
                if param == 'request' and val=="":
                    val = rq
                elif param == 'remote_addr':
                    val = rq.META['REMOTE_ADDR']
                if param in keys:
                    args.append(val) #if val=='': val=None
                elif isAwgs:
                    awgs[param] = val
                
            #if param=='token' and val in staticTokenCache:
            #    rq.environ['HTTP_X_USER_ID'] = staticTokenCache[val]['user_id']
                
        if attrs and isAwgs:
            for attr in d:
                if attr not in keysL:
                    awgs[attr] = d[attr]

        try:
            rs = fn(*args, **awgs)
        except TypeError:
            strd = str(d)
            #if len(strd)<10000: print(strd)
            #saveErrCaller()
            print(traceback.format_exc())
            raise  
        return  rs



        
if __name__ == "__main__":
    import doctest
    doctest.testmod() #verbose=True
    























    