import streamlit as st
import random
from time import sleep
import base64
from io import BytesIO
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# 设置页面配置
st.set_page_config(
    page_title="jwx专属奶茶选择器",
    page_icon="🧋",
    layout="centered"
)

# 隐藏默认的Streamlit样式
hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# 自定义CSS样式
custom_css = """
<style>
    /* 主标题样式 */
    .main-title {
        font-size: 4rem !important;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        text-shadow: 3px 3px 0 #FFD166, 6px 6px 0 #06D6A0;
        margin-bottom: 2rem;
        animation: pulse 2s infinite;
    }

    /* 心情按钮样式 */
    .mood-btn {
        width: 100%;
        padding: 1.5rem 0;
        margin: 1rem 0;
        font-size: 1.5rem !important;
        font-weight: bold;
        border-radius: 50px !important;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    .mood-btn:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    /* 品牌卡片样式 */
    .brand-card {
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .brand-card:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }

    /* 动画效果 */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }

    .angry-emoji {
        font-size: 3rem;
        animation: shake 0.5s infinite;
    }

    @keyframes shake {
        0% { transform: rotate(0deg); }
        25% { transform: rotate(10deg); }
        50% { transform: rotate(0deg); }
        75% { transform: rotate(-10deg); }
        100% { transform: rotate(0deg); }
    }

    /* 全屏特效样式 */
    .full-screen-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        background: rgba(255,255,255,0.9);
        animation: fadeIn 0.5s ease;
    }

    .happy-text {
        font-size: 8rem;
        font-weight: bold;
        color: #FF6B6B;
        animation: float 3s infinite, pulse 2s infinite;
        text-shadow: 8px 8px 0 #FFD166;
    }

    .angry-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: 1rem;
        width: 100%;
        height: 100%;
        padding: 2rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 初始化session状态
if 'mood' not in st.session_state:
    st.session_state.mood = None
if 'selected_brand' not in st.session_state:
    st.session_state.selected_brand = None
if 'show_effect' not in st.session_state:
    st.session_state.show_effect = False
if 'game_active' not in st.session_state:
    st.session_state.game_active = False

# 奶茶品牌数据
BRAND_DATA = {
    "古茗": {
        "recommendations": [
            {"name": "芝士葡萄", "reason": "新鲜葡萄搭配香浓芝士，带来清爽与满足的双重享受"},
            {"name": "杨枝甘露", "reason": "芒果与椰奶的完美融合，加入西柚粒增添清新口感"},
            {"name": "芋泥波波奶茶", "reason": "手工熬制的芋泥搭配Q弹波波，温暖你的心"}
        ]
    },
    "茶百道": {
        "recommendations": [
            {"name": "豆乳玉麒麟", "reason": "豆乳奶盖与茶底的绝妙搭配，口感层次丰富"},
            {"name": "杨枝甘露", "reason": "经典港式甜品风味，果香浓郁回味无穷"},
            {"name": "茉莉奶绿", "reason": "清新茉莉花香与醇厚鲜奶的完美结合"}
        ]
    },
    "爷爷不泡茶": {
        "recommendations": [
            {"name": "爷爷奶茶", "reason": "招牌经典，传承多年的独特配方"},
            {"name": "荔枝冰茶", "reason": "当季新鲜荔枝果肉，带来夏日清凉"},
            {"name": "草莓奶芙", "reason": "草莓果肉搭配绵密奶芙，少女心满满"}
        ]
    },
    "蜜雪冰城": {
        "recommendations": [
            {"name": "冰鲜柠檬水", "reason": "超值解渴神器，清爽一整天"},
            {"name": "草莓摇摇奶昔", "reason": "草莓果酱与冰淇淋的完美融合"},
            {"name": "珍珠奶茶", "reason": "经典款永不过时，平价中的战斗机"}
        ]
    },
    "瑞幸咖啡": {
        "recommendations": [
            {"name": "生椰拿铁", "reason": "网红爆款，椰香与咖啡的完美邂逅"},
            {"name": "厚乳拿铁", "reason": "浓郁奶香，咖啡爱好者的首选"},
            {"name": "陨石拿铁", "reason": "黑糖风味与咖啡的独特碰撞"}
        ]
    }
}


# 创建开心特效图像
def create_happy_effect_image():
    # 创建一个透明背景的图像
    img = Image.new('RGBA', (800, 400), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 使用大号字体绘制"开心!"文本
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()

    # 绘制带有阴影的文本
    draw.text((202, 152), "开 心 !", fill="black", font=font)
    draw.text((200, 150), "开 心 !", fill="#FF6B6B", font=font)

    # 添加一些装饰元素
    for i in range(20):
        x = random.randint(0, 800)
        y = random.randint(0, 400)
        size = random.randint(10, 50)
        draw.ellipse([(x, y), (x + size, y + size)], fill="#FFD166", outline="#06D6A0")

    return img


# 创建愤怒表情包图像
def create_angry_effect_image():
    # 创建一个白色背景的图像
    img = Image.new('RGB', (800, 600), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 在网格中填充愤怒表情
    emoji_size = 60
    for row in range(10):
        for col in range(15):
            x = col * emoji_size + 10
            y = row * emoji_size + 10

            # 绘制旋转的表情符号
            angle = random.randint(-20, 20)
            rotated_emoji = Image.new('RGBA', (emoji_size, emoji_size), (255, 255, 255, 0))
            d = ImageDraw.Draw(rotated_emoji)
            d.text((20, 20), "😠", fill="black", font=ImageFont.load_default())
            rotated_emoji = rotated_emoji.rotate(angle, expand=True)

            # 将旋转后的表情粘贴到主图像
            img.paste(rotated_emoji, (x, y), rotated_emoji)

    return img


# 显示全屏开心特效
def show_happy_effect():
    # 创建图像
    img = create_happy_effect_image()

    # 将图像转换为Base64以便在HTML中使用
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # 显示全屏覆盖
    st.markdown(
        f"""
        <div class="full-screen-overlay">
            <img src="data:image/png;base64,{img_str}" style="max-width: 100%; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )

    # 等待3秒
    sleep(3)
    st.session_state.show_effect = False
    st.rerun()


# 显示愤怒表情包
def show_angry_effect():
    # 创建图像
    img = create_angry_effect_image()

    # 将图像转换为Base64以便在HTML中使用
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # 显示全屏覆盖
    st.markdown(
        f"""
        <div class="full-screen-overlay">
            <img src="data:image/png;base64,{img_str}" style="max-width: 100%; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )

    # 等待3秒
    sleep(3)
    st.session_state.show_effect = False
    st.rerun()


# 贪吃蛇小游戏
def snake_game():
    st.session_state.game_active = True

    # 游戏初始化
    if 'snake' not in st.session_state:
        st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
        st.session_state.direction = "RIGHT"
        st.session_state.food = (random.randint(0, 9), random.randint(0, 9))
        st.session_state.score = 0
        st.session_state.game_over = False

    # 游戏控制
    cols = st.columns(4)
    with cols[1]:
        if st.button("↑", key="up", use_container_width=True):
            if st.session_state.direction != "DOWN":
                st.session_state.direction = "UP"
    with cols[0]:
        if st.button("←", key="left", use_container_width=True):
            if st.session_state.direction != "RIGHT":
                st.session_state.direction = "LEFT"
    with cols[2]:
        if st.button("→", key="right", use_container_width=True):
            if st.session_state.direction != "LEFT":
                st.session_state.direction = "RIGHT"
    with cols[3]:
        if st.button("↓", key="down", use_container_width=True):
            if st.session_state.direction != "UP":
                st.session_state.direction = "DOWN"

    # 游戏逻辑
    if not st.session_state.game_over:
        head_x, head_y = st.session_state.snake[0]

        if st.session_state.direction == "UP":
            head_x -= 1
        elif st.session_state.direction == "DOWN":
            head_x += 1
        elif st.session_state.direction == "LEFT":
            head_y -= 1
        elif st.session_state.direction == "RIGHT":
            head_y += 1

        # 检查碰撞
        if head_x < 0 or head_x >= 10 or head_y < 0 or head_y >= 10 or (head_x, head_y) in st.session_state.snake:
            st.session_state.game_over = True
        else:
            new_head = (head_x, head_y)
            st.session_state.snake.insert(0, new_head)

            # 检查是否吃到食物
            if new_head == st.session_state.food:
                st.session_state.score += 1
                # 生成新食物（确保不在蛇身上）
                while True:
                    st.session_state.food = (random.randint(0, 9), random.randint(0, 9))
                    if st.session_state.food not in st.session_state.snake:
                        break
            else:
                st.session_state.snake.pop()

    # 游戏显示
    st.markdown(f"<h2 style='text-align: center;'>贪吃蛇小游戏 - 得分: {st.session_state.score}</h2>",
                unsafe_allow_html=True)

    if st.session_state.game_over:
        st.error("游戏结束! 你的最终得分: {}".format(st.session_state.score))
        if st.button("重新开始游戏", use_container_width=True):
            st.session_state.game_active = False
            del st.session_state.snake
            st.rerun()
    else:
        # 创建游戏网格
        grid = [['⬜' for _ in range(10)] for _ in range(10)]

        # 放置食物
        food_x, food_y = st.session_state.food
        grid[food_x][food_y] = '🍎'

        # 放置蛇
        for i, (x, y) in enumerate(st.session_state.snake):
            grid[x][y] = '🟩' if i == 0 else '🟢'

        # 显示游戏网格
        game_html = "<div style='font-size: 24px; line-height: 30px; text-align: center;'>"
        for row in grid:
            game_html += "".join(row) + "<br>"
        game_html += "</div>"

        st.markdown(game_html, unsafe_allow_html=True)

        # 自动刷新游戏
        sleep(0.2)
        st.rerun()


# 主应用
st.markdown("<h1 class='main-title'>jwx专属奶茶选择器</h1>", unsafe_allow_html=True)

# 显示心情选择
if st.session_state.mood is None and not st.session_state.game_active and not st.session_state.show_effect:
    st.subheader("今天心情如何？", anchor=False)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("😖 不好", key="bad", use_container_width=True,
                     help="心情不好？来杯奶茶治愈一下吧！",
                     type="primary"):
            st.session_state.mood = "bad"
            st.rerun()

    with col2:
        if st.button("😐 一般", key="normal", use_container_width=True,
                     help="心情一般？玩个小游戏放松一下吧！",
                     type="primary"):
            st.session_state.mood = "normal"
            st.rerun()

    with col3:
        if st.button("😊 还可以", key="good", use_container_width=True,
                     help="心情还可以？来点小惊喜！",
                     type="primary"):
            st.session_state.mood = "good"
            st.rerun()

    with col4:
        if st.button("😄 非常好", key="excellent", use_container_width=True,
                     help="心情非常好？保持住！",
                     type="primary"):
            st.session_state.mood = "excellent"
            st.rerun()

# 心情不好时的品牌选择
if st.session_state.mood == "bad" and not st.session_state.selected_brand and not st.session_state.show_effect:
    st.subheader("喝杯奶茶治愈一下吧！", anchor=False)
    st.info("心情不好时，来杯奶茶最治愈！选一个你喜欢的品牌：")

    # 显示品牌选择卡片
    for brand in ["古茗", "茶百道", "爷爷不泡茶", "蜜雪冰城", "瑞幸咖啡"]:
        if st.button(f"选择 {brand}", key=f"brand_{brand}", use_container_width=True):
            st.session_state.selected_brand = brand
            st.session_state.show_effect = True
            st.rerun()

        with st.expander(f"{brand} 推荐菜单", expanded=False):
            for item in BRAND_DATA[brand]["recommendations"]:
                st.markdown(f"**{item['name']}** - {item['reason']}")

    # 添加微信发swj请吃小蛋糕
    if st.button("微信发swj请吃小蛋糕", key="cake", use_container_width=True):
        st.session_state.selected_brand = "微信发swj请吃小蛋糕"
        st.session_state.show_effect = True
        st.rerun()

    st.markdown("""
        <div style="background-color: #FFF9C4; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
            <p>有时候一杯奶茶不够，还需要甜蜜的小蛋糕来治愈！</p>
            <p>快给swj发消息："心情不好，求小蛋糕治愈！" 🍰</p>
        </div>
    """, unsafe_allow_html=True)

# 心情一般时的处理
elif st.session_state.mood == "normal" and not st.session_state.show_effect:
    if not st.session_state.game_active:
        st.subheader("来杯奶茶提提神吧！", anchor=False)
        st.warning("心情一般时，简单的快乐最有效！推荐这两个品牌：")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("蜜雪冰城")
            for item in BRAND_DATA["蜜雪冰城"]["recommendations"]:
                st.markdown(f"**{item['name']}** - {item['reason']}")

        with col2:
            st.subheader("瑞幸咖啡")
            for item in BRAND_DATA["瑞幸咖啡"]["recommendations"]:
                st.markdown(f"**{item['name']}** - {item['reason']}")

        st.success("选好了奶茶，现在玩个小游戏放松一下吧！")

        if st.button("开始玩贪吃蛇游戏", use_container_width=True, type="primary"):
            st.session_state.game_active = True
            st.rerun()
    else:
        snake_game()

# 心情还可以时的处理
elif st.session_state.mood == "good" and not st.session_state.show_effect:
    st.subheader("心情不错哦！", anchor=False)
    st.warning("既然心情还可以，那就来点特别的吧！")

    if st.button("点击获取惊喜", use_container_width=True, type="primary"):
        st.session_state.show_effect = True
        st.rerun()

    if st.session_state.show_effect:
        show_happy_effect()

# 心情非常好时的处理
elif st.session_state.mood == "excellent" and not st.session_state.show_effect:
    st.subheader("心情这么好还想喝奶茶？", anchor=False)
    st.error("心情已经非常好了，再喝奶茶小心挨骂哦！")

    if st.button("我就要喝！", use_container_width=True, type="primary"):
        st.session_state.show_effect = True
        st.rerun()

    if st.session_state.show_effect:
        show_angry_effect()

# 品牌选择后的全屏特效
if st.session_state.selected_brand and st.session_state.mood == "bad" and not st.session_state.show_effect:
    st.session_state.show_effect = True
    st.rerun()

if st.session_state.show_effect and st.session_state.mood == "bad":
    show_happy_effect()

# 添加重置按钮
if st.session_state.mood or st.session_state.game_active:
    if st.button("重新选择心情", use_container_width=True):
        st.session_state.mood = None
        st.session_state.selected_brand = None
        st.session_state.show_effect = False
        st.session_state.game_active = False
        if 'snake' in st.session_state:
            del st.session_state.snake
        st.rerun()