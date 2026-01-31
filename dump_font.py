### dump_font.py
### 从 光荣三国志2 DOS中文版的 font.dat 中导出所有字模，生成字体图集 font_sheet.png

from PIL import Image

FILENAME = "font.dat"

TILE_STRIDE = 30
TILE_DATA = 28
START_OFFSET = 2

WIDTH = 16
HEIGHT = 14

SCALE = 4        # 放大倍数（可改 2 / 4 / 8）
TILES_PER_ROW = 32   # 每行多少字


def read_tile(data, index):
    start = START_OFFSET + index * TILE_STRIDE
    return data[start:start + TILE_DATA]


def draw_tile(img, tile, ox, oy):
    for row in range(HEIGHT):
        b0 = tile[row * 2]
        b1 = tile[row * 2 + 1]

        for col in range(8):
            if (b0 >> (7 - col)) & 1:
                for dx in range(SCALE):
                    for dy in range(SCALE):
                        img.putpixel(
                            (ox + col * SCALE + dx,
                             oy + row * SCALE + dy),
                            (0, 0, 0)
                        )

        for col in range(8):
            if (b1 >> (7 - col)) & 1:
                x = 8 + col
                for dx in range(SCALE):
                    for dy in range(SCALE):
                        img.putpixel(
                            (ox + x * SCALE + dx,
                             oy + row * SCALE + dy),
                            (0, 0, 0)
                        )


def main():
    with open(FILENAME, "rb") as f:
        data = f.read()

    total = (len(data) - START_OFFSET) // TILE_STRIDE
    print("Total tiles:", total)

    rows = (total + TILES_PER_ROW - 1) // TILES_PER_ROW

    img = Image.new(
        "RGB",
        (TILES_PER_ROW * WIDTH * SCALE,
         rows * HEIGHT * SCALE),
        "white"
    )

    for i in range(total):
        tile = read_tile(data, i)

        tx = i % TILES_PER_ROW
        ty = i // TILES_PER_ROW

        ox = tx * WIDTH * SCALE
        oy = ty * HEIGHT * SCALE

        draw_tile(img, tile, ox, oy)

    img.save("font_sheet.png")
    print("saved font_sheet.png")


if __name__ == "__main__":
    main()
