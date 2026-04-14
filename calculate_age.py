#!/usr/bin/env python3
"""
根据出生年份计算年龄
输入出生年份，输出 "你今年XX岁了！"
"""

from datetime import datetime


def calculate_age(birth_year: int) -> str:
    """
    根据出生年份计算年龄，并返回格式化字符串

    Args:
        birth_year: 出生年份（四位数，例如 1999）

    Returns:
        格式化字符串，例如 "你今年27岁了！"
    """
    current_year = datetime.now().year
    age = current_year - birth_year
    return f"你今年{age}岁了！"


def main():
    """主函数，交互模式运行"""
    try:
        birth_year_input = input("请输入出生年份（例如1999）: ")
        birth_year = int(birth_year_input)
        result = calculate_age(birth_year)
        print(result)
    except ValueError:
        print("输入错误，请输入有效的年份数字（例如 1999）")


if __name__ == "__main__":
    main()
