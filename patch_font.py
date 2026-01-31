### patch_font.py
### 将 光荣三国志2 PC-98 日文版的 font.dat 中的某一个汉字字模，替换为自己需要的，同时生成预览图 daji_preview.png

from PIL import Image, ImageDraw, ImageFont

FONT_DAT = "font.dat"
CHAR = "妲"

WIDTH = 16
HEIGHT = 16
BYTES_PER_TILE = 32   # 16行 × 每行2字节

# 改成自己电脑上真实存在的字体
FONT_PATH = "C:/Windows/Fonts/simsun.ttc"


def render_char():
    img = Image.new("L", (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(FONT_PATH, 16)

    bbox = draw.textbbox((0, 0), CHAR, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((WIDTH - w) // 2, (HEIGHT - h) // 2), CHAR, font=font, fill=0)

    return img


def image_to_pc98_bytes(img):
    data = bytearray()

    for y in range(HEIGHT):
        left = 0
        right = 0

        for x in range(8):
            if img.getpixel((x, y)) < 128:
                left |= 1 << (7 - x)

        for x in range(8):
            if img.getpixel((8 + x, y)) < 128:
                right |= 1 << (7 - x)

        data.append(left)
        data.append(right)

    return bytes(data)


def main():
    with open(FONT_DAT, "rb") as f:
        raw = bytearray(f.read())

    total = len(raw) // BYTES_PER_TILE
    index = total - 1  # FONT.DAT 字库中要被替换掉的，倒数第1个汉字

    print("Total tiles:", total)
    print("Patching index:", index)

    offset = index * BYTES_PER_TILE

    img = render_char()
    tile = image_to_pc98_bytes(img)

    raw[offset:offset+32] = tile

    with open(FONT_DAT, "wb") as f:
        f.write(raw)

    img.save("daji_preview.png")
    print("完成：已替换为 妲")
    print("生成预览：daji_preview.png")


if __name__ == "__main__":
    main()
