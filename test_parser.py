from parser import parse_questions

test_text = """1. (单选题) 以下哪个是Python的基本数据类型？
A. 整数
B. 字符串
C. 列表
D. 以上都是
正确答案：D
我的答案：C

2. (填空题) Python中用于定义函数的关键字是【def】。
正确答案：def
我的答案：function

3. (判断题) Python是解释型语言。
正确答案：正确
我的答案：错误

4. (多选题) 以下哪些是Python的内置函数？
A. print()
B. len()
C. max()
D. 以上都是
正确答案：D
我的答案：A"""

result = parse_questions(test_text)
print(f"解析成功！共找到 {result['total']} 道题目")
print("\n题目详情：")
for q in result['questions']:
    print(f"\n题目 {q['id']} ({q['type']}):")
    print(f"  题干: {q['question']}")
    if q['options']:
        print(f"  选项: {q['options']}")
    print(f"  正确答案: {q['correct_answer']}")
    print(f"  我的答案: {q['user_answer']}")