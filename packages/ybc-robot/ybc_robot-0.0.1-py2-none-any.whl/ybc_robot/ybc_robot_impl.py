import sys

from ybc_commons.ArgumentChecker import Checker
from ybc_commons.ArgumentChecker import Argument
from ybc_commons.util.predicates import is_greater_or_equal
from ybc_commons.util.predicates import is_in

if sys.platform == 'skulpt':
    import ybc_lib_skulpt_robot as lib_ybc_robot
else:
    raise NotImplementedError("ybc_robot 模块仅在 skulpt 环境下运行")


def forward(number: int = 1):
    """
    向前走

    :param number: 执行前进的次数 (整数,非必填) 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'forward', 'number', number, int, is_greater_or_equal(0))
    ])
    lib_ybc_robot.forward(number)


def left(number: int = 1):
    """
    向左转

    :param number: 执行左转的次数 (整数,非必填) 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'left', 'number', number, int, is_greater_or_equal(0))
    ])
    lib_ybc_robot.left(number)


def right(number: int = 1):
    """
    向左转

    :param number: 执行右转的次数 (整数,非必填) 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'right', 'number', number, int, is_greater_or_equal(0))
    ])
    lib_ybc_robot.left(number)


def head(number: int = 1):
    """
    选择头的造型

    :param number: 选择不同的造型 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'head', 'number', number, int, is_in({1, 2, 3}))
    ])
    lib_ybc_robot.head(number)


def body(number: int = 1):
    """
    选择身体的造型

    :param number: 选择不同的造型 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'body', 'number', number, int, is_in({1, 2, 3}))
    ])
    lib_ybc_robot.head(number)


def leg(number: int = 1):
    """
    选择腿的造型

    :param number: 选择不同的造型 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'leg', 'number', number, int, is_in({1, 2, 3}))
    ])
    lib_ybc_robot.leg(number)


def switch(number: int = 1):
    """

    :param number: 表示执行相应事件的次数(非必填) 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'switch', 'number', number, int, is_greater_or_equal(0))
    ])
    lib_ybc_robot.switch(number)


def wave(number: int = 1):
    """

    :param number: 表示执行相应事件的次数(非必填) 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'wave', 'number', number, int, is_greater_or_equal(0))
    ])
    lib_ybc_robot.wave(number)


def nod(number: int = 1):
    """

    :param number: 表示执行相应事件的次数(非必填) 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'nod', 'number', number, int, is_greater_or_equal(0))
    ])
    lib_ybc_robot.nod(number)


def rock(number: int = 1):
    """

    :param number: 表示执行相应事件的次数(非必填) 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'rock', 'number', number, int, is_greater_or_equal(0))
    ])
    lib_ybc_robot.rock(number)


def heart(number: int = 1):
    """

    :param number: 表示执行相应事件的次数(非必填) 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'heart', 'number', number, int, is_greater_or_equal(0))
    ])
    lib_ybc_robot.heart(number)


def detect():
    """
    检测当前格子所在颜色

    :param : 无
    :return: 返回字符串
    """
    return lib_ybc_robot.detect()


def build(number: int = 1):
    """

    :param number: 表示执行相应事件的次数(非必填) 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'build', 'number', number, int, is_greater_or_equal(0))
    ])
    return lib_ybc_robot.build(number)


def destroy(number: int = 1):
    """

    :param number: 表示执行相应事件的次数(非必填) 例子：1
    :return: 无返回值
    """
    Checker.check_arguments([
        Argument('ybc_robot', 'destroy', 'number', number, int, is_greater_or_equal(0))
    ])
    return lib_ybc_robot.destroy(number)
