import re
import glob
import os

__root_dir = os.path.join(os.path.dirname(__file__), "..")


def camel_to_snake(name: str) -> str:
    """
    将小驼峰命名转换为蛇形命名（保留前缀下划线）

    Args:
        name: 输入的小驼峰字符串（允许带前缀下划线，如 __myVar）

    Returns:
        转换后的蛇形字符串（如 __my_var）

    Example:
        >>> camel_to_snake("firstName")
        "first_name"
        >>> camel_to_snake("__myVar123")
        "__my_var123"
        >>> camel_to_snake("getHTTPResponse")
        "get_http_response"
    """
    # 分离前缀下划线（保留所有前缀 _）
    prefix = name[: len(name) - len(name.lstrip("_"))]
    suffix = name.lstrip("_")

    # 核心转换逻辑：在大写字母前加下划线，并转全小写
    # 使用正则 (?<!^) 确保不在开头加下划线，避免首字母被处理
    transformed = re.sub(r"(?<!^)(?=[A-Z])", "_", suffix).lower()

    return prefix + transformed


def is_inside_quotes(line: str, start_pos: int, word: str) -> bool:
    """
    检查指定位置是否在引号包裹范围内（支持转义字符处理）
    """

    start_char = line[start_pos - 1]
    end_char = line[start_pos + len(word)]

    if start_char == " " or end_char == " ":
        return True


def find_lower_camel_in_file(file_path: str):
    """
    从文件中提取所有小驼峰命名（忽略引号包裹的字符串）

    规则：
    1. 允许任意数量下划线前缀（如 _myVar、__specialCase）
    2. 首字母必须小写（去除前缀后）
    3. 必须包含至少一个大写字母
    4. 不能包含下划线（除前缀外）
    5. 排除全小写的情况
    """
    # 候选词正则：匹配可能的前导下划线+小写字母开头的单词
    candidate_pattern = re.compile(r"\b_*[a-z]\w*\b")  # 宽松匹配候选词

    def is_lower_camel(s: str) -> bool:
        # 剥离所有前缀下划线
        s_clean = s.lstrip("_")
        # 校验规则
        return (
            len(s_clean) > 0
            and s_clean[0].islower()
            and any(c.isupper() for c in s_clean)
            and "_" not in s_clean
            and s_clean.isalnum()
        )

    # 逐行扫描文件
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            # 查找所有候选词
            for match in candidate_pattern.finditer(line):
                word = match.group()
                start_pos = match.start()
                # 排除引号内的内容
                if is_inside_quotes(line, start_pos, word):
                    if is_lower_camel(word):
                        print(
                            f"{file_path}:{line_num}: {word} -> {camel_to_snake(word)}"
                        )


# 使用示例
if __name__ == "__main__":

    py_files = glob.glob(f"{__root_dir}/**/*.py", recursive=True)
    for file in py_files:
        if not file.endswith("_ui.py"):
            find_lower_camel_in_file(file)
    # import sys

    # if len(sys.argv) != 2:
    #     print("Usage: python find_camel.py <file_path>")
    #     sys.exit(1)
    # find_lower_camel_in_file(sys.argv[1])
