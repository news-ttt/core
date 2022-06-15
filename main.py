# 1. 深度合并
import traceback
def merge_dict(source_dict, update_dict):
    for k, v in update_dict.items():
        if k not in source_dict:
            source_dict[k] = v
        elif type(v) != type(source_dict[k]):
            raise TypeError(f"两个字典中{k}类型不一致，不可合并")
        elif isinstance(v, dict):
            source_dict[k].update(v)
        else:
            source_dict[k] = v
    return source_dict

# source_dict = { 'key0': 'a', 'key1': 'b', 'key2': { 'inner_key0': 'c', 'inner_key1': 'd' }, "key3": "33" }
# update_dict = { 'key1': 'x', 'key2': { 'inner_key0': 'y' }, "key3": 1 }
source_dict = { 'key0': 'a', 'key1': 'b', 'key2': { 'inner_key0': 'c', 'inner_key1': 'd' } }
update_dict = { 'key1': 'x', 'key2': { 'inner_key0': 'y' } }
try:
    result = merge_dict(source_dict, update_dict)
    print(result)
except TypeError as e:
    print(e)
except Exception as e:
    print('深度合并报错，参数 source_dict:{} update_dict{}, 错误{}'.format(source_dict, update_dict, traceback.format_exc()))


# 2.电子组合排序

# 情况1 返回的是双字母组合
def connect(x, y, res=[]):
    for i in x:
        for j in y:
            res.append(i+j)
    return res
def phoneLetter(s):
    res = []
    letter = ["", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]
    if not s:
        return res
    if not s.isdigit():
        return "字符串非2-9纯数字"
    if len(s) == 1:
        return (letter[int(s)])
    lens = len(s)
    for i in range(0, lens):
        for j in range(i+1, lens):
            res = connect(letter[int(s[i])], letter[int(s[j])])
    return res
print(phoneLetter("234"))

# 情况2 返回多个字母组合
def phoneLetter2(s):
    res = []
    letter = ["", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]
    if not s:
        return res
    if not s.isdigit():
        return "字符串非2-9纯数字"
    if len(s) == 1:
        return (letter[int(s)])
    lens = len(s)
    res = connect(letter[int(s[0])], letter[int(s[1])], res)
    if lens == 2:
        return res
    else:
        for i in range(2, lens):
            res = connect(res, letter[int(s[i])], [])
    return res

print(phoneLetter2("2345"))
# 3.内存泄漏
# 理解： 以前没有遇到过这种问题，刚才百度恶补了下，我对内存泄露的理解如下：
    # 1. 代码中⽤到了全局的 list、 dict 或其它容器，不停的往这些容器中插⼊对象，⽽忘记了在使⽤完之后进⾏删除回收
    # 2. 代码中有“引⽤循环”，并且被循环引⽤的对象定义了__del__⽅法，就会发⽣内存泄露

import sys
class A:
	def __init__(self):
		self.a = None


def func():
	a1 = A()
	a2 = A()
	a3 = A()
	print('a1/a2引用计数为2')
	print('a1:',sys.getrefcount(a1))
	a1.a = a2
	a2.a = a1
	print('a1:',sys.getrefcount(a1))
	a3.a = a1
	print('a1:',sys.getrefcount(a1))
	del a3 # 删除a3同时减少a1的引用计数
	print('a1:',sys.getrefcount(a1))

	print(id(a2.a))
	return
	# 这个执行之后，a3引用计数满足内存释放条件
	# a1,a2 引用计数不满足内存释放条件
func()
# 执行到此，a3被回收（或者可回收状态），而a1,a2用由于相互引用，在函数func执行完之后而不能够被回收，变成不可管理的垃圾内存