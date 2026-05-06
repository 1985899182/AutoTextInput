import pyautogui
import time
import os

os.system("title 键盘自动输入工具")

ARTICLE = """
In this era of globalization, the ability to communicate across cultures has become essential for college students. Organizing forums on this topic is both timely and highly worthwhile.
Effective cross-cultural communication allows us to interact more smoothly with people from diverse backgrounds. It helps prevent unnecessary misunderstandings and conflicts that often arise from differences in customs, values, and ways of living. Moreover, this skill has become increasingly important for career development. As more companies engage in international collaboration, graduates who can navigate cultural differences tend to adapt faster and perform better in global work environments.
Beyond practical benefits, exposure to different cultures broadens our perspectives. It strengthens our tolerance, flexibility, and adaptability while encouraging us to think in new ways. Through such interactions, we often become more open-minded and self-aware.
In conclusion, strong cross-cultural communication skills enrich our academic life, personal growth, and future opportunities. Rather than waiting for chances to appear, we should actively participate in multicultural activities—whether through exchange programs, international clubs, or cultural events. Only by doing so can we truly thrive in an interconnected world.
"""

def type_article(text, interval=0.02):
    print("=" * 50)
    print(f" 文本长度: {len(text)} 字符")
    print(f" 输入间隔: {interval} 秒/字符")
    print("=" * 50)
    print("\n[!!] 5秒后开始输入，请立即切换到目标窗口！\n")

    for i in range(5, 0, -1):
        print(f"  倒计时: {i} ...")
        time.sleep(1)

    print("\n[>>] 开始输入...\n")
    pyautogui.typewrite(text, interval=interval)
    print("\n[OK] 输入完成！")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════╗
║     键盘自动输入工具 v1.0            ║
║     用于绕过禁止复制粘贴的网页       ║
╚══════════════════════════════════════╝

使用说明:
1. 先修改代码中的 ARTICLE 变量，填入你的英文文章
2. 运行脚本后，会有 5 秒倒计时
3. 在倒计时期间切换到目标网页/输入框
4. 脚本会自动模拟键盘逐字输入
5. 如需紧急停止，将鼠标快速移到屏幕四角即可

注意事项:
- interval 参数控制输入速度(秒)，默认0.02
- 某些网站检测过快可调大间隔(如0.05)
- 仅支持英文字符和常见标点
""")

    type_article(ARTICLE, interval=0.02)
