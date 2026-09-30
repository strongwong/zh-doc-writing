#!/usr/bin/env python3
"""扫描中文文档里常见的 AI 腔词语和格式问题，输出 文件:行号 [类别] 命中。

只做字面匹配，结果需要人工判断。跳过 ``` 代码块和行内代码。
用法：ai_scan.py <file> [<file> ...]
"""
import re
import sys

RULES = [
    ("开头铺垫", r"随着.{0,20}的(快速|不断|飞速|迅速)?发展|在当今|众所周知|本文将|接下来(我们)?将|下面(我们)?来|让我们"),
    ("结尾复述", r"综上所述|总的来说|总而言之|总之，|通过以上.{0,10}(可以看出|分析)|希望(本文|这篇|以上)?.{0,6}(对你|对您|能)有(所)?帮助|欢迎(交流|讨论|指正)"),
    ("拔高词", r"至关重要|不可或缺|举足轻重|重要意义|核心价值|关键作用|奠定.{0,4}基础|里程碑|新篇章|新阶段"),
    ("宣传词", r"强大的|无缝|全方位|极致|优雅地?|卓越|一站式|开箱即用|轻松(实现|应对|搞定)|显著(提升|提高|降低)|大幅(提升|提高|降低)"),
    ("黑话", r"赋能|助力|抓手|闭环|沉淀|对齐|颗粒度|打通|底层逻辑|范式|心智|链路"),
    ("书面虚词", r"旨在|致力于|彰显|凸显|切实|深入(分析|探讨|了解)|充分(利用|发挥)|有效(提升|提高|降低|保障|避免)"),
    ("翻译腔", r"进行(了)?(修改|校验|检查|分析|处理|配置|优化|测试|验证|调整|初始化)|对.{1,15}进行|通过.{1,15}的方式|作为一(个|名|种)|使得"),
    ("否定对比", r"不是.{1,30}而是|不仅.{1,30}(而且|更|还)|与其说.{1,20}不如说"),
    ("设问自答", r"(原因|答案|道理|关键)(很简单|在于)[:：]|为什么(会)?这样[?？]|关键是什么[?？]"),
    ("同义重复", r"简单来说|换句话说|也就是说|换言之"),
    ("模糊归因", r"业界普遍|有研究表明|研究显示|很多(开发者|用户|人)(认为|反馈)|普遍认为"),
    ("过度含糊", r"在某种程度上|在一定(程度|情况)下|某种意义上"),
    ("万能句尾", r"从而(确保|保证|提升|实现)|确保.{0,10}(稳定性|可靠性|安全性)(和|与)"),
    ("比喻拟人", r"就像.{1,20}一样|可以(把它)?想象成|如同一|聪明地|贴心地"),
]

FORMAT_RULES = [
    ("感叹号", r"[!！]"),
    ("破折号", r"——|—"),
    ("emoji", r"[\U0001F300-\U0001FAFF☀-➿⭐✅❌]"),
    ("加粗标签列表", r"^\s*[-*+]\s+\*\*[^*]+\*\*\s*[:：]"),
    ("非标准省略号", r"\.\.\.|。。。|⋯"),
]

INLINE_CODE = re.compile(r"`[^`]*`")


def scan(path):
    hits = []
    dash_lines = []
    in_code = False
    with open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            if raw.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            line = INLINE_CODE.sub("", raw.rstrip("\n"))
            for cat, pat in RULES + FORMAT_RULES:
                for m in re.finditer(pat, line):
                    if cat == "感叹号" and m.group() == "!" and line[m.end():m.end() + 1] == "[":
                        continue  # Markdown 图片 ![...]
                    hits.append((lineno, cat, m.group()))
                    if cat == "破折号":
                        dash_lines.append(lineno)
    for lineno, cat, text in hits:
        print(f"{path}:{lineno}: [{cat}] {text}")
    if len(dash_lines) > 2:
        print(f"{path}: 破折号共 {len(dash_lines)} 处，建议全文不超过 2 处")
    return len(hits)


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    total = sum(scan(p) for p in sys.argv[1:])
    print(f"共 {total} 处命中" if total else "未发现命中")
    return 0


if __name__ == "__main__":
    sys.exit(main())
