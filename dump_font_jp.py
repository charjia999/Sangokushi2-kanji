### dump_font_jp.py
### 从 光荣三国志2 PC-98 日文版的 font.dat 中导出所有字模，生成字体图集 font_sheet_jp.png
from PIL import Image

FILENAME = "font.dat"

WIDTH = 16
HEIGHT = 16

BYTES_PER_TILE = 32

SCALE = 4
TILES_PER_ROW = 32


def read_tile(data, index):
    start = index * BYTES_PER_TILE
    return data[start:start + BYTES_PER_TILE]


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

    total = len(data) // BYTES_PER_TILE
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

    img.save("font_sheet_jp.png")
    print("saved font_sheet_jp.png")


if __name__ == "__main__":
    main()
