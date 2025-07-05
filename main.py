import random


def guess_the_number():
    # 生成随机数字
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7

    print("欢迎来到猜数字游戏！")
    print(f"我已经想好了1~100之间的一个数字，你有{max_attempts}次机会猜中它。")

    while attempts < max_attempts:
        try:
            # 获取用户输入
            guess = int(input("\n请输入你的猜测: "))
            attempts += 1

            # 判断猜测结果
            if guess < secret_number:
                print(f"太小了！还剩 {max_attempts - attempts} 次机会")
            elif guess > secret_number:
                print(f"太大了！还剩 {max_attempts - attempts} 次机会")
            else:
                print(f"恭喜！你在第{attempts}次猜中了答案 {secret_number}！")
                return

        except ValueError:
            print("请输入有效的整数！")

    print(f"\n游戏结束！正确答案是: {secret_number}")


# 启动游戏
if __name__ == "__main__":
    guess_the_number()