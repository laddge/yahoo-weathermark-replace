import toml
from PIL import Image

imgs = {}


def getimg(name):
    if name in imgs.keys():
        return imgs[name]
    else:
        img = Image.open(f"./src/base/{name}.png").convert("RGBA")
        imgs[name] = img
        return img


def edit(args):
    if args[0] == "half":
        fg = getimg(args[1])
        bg = getimg(args[2])
        bg = bg.resize((int(bg.width * fg.height / bg.height * 0.9), int(fg.height * 0.9)))
        bg_base = Image.new(
            "RGBA", (int((bg.width + fg.width) * 0.8), fg.height), (0,) * 4
        )
        fg_base = bg_base.copy()
        bg_base.paste(bg, (bg_base.width - bg.width, 0))
        fg_base.paste(fg, (0, 0))
        return Image.alpha_composite(bg_base, fg_base)
    elif args[0] == "qurt":
        bg = getimg(args[1])
        fg = getimg(args[2])
        fg = fg.resize(
            (int(fg.width * bg.height / fg.height * 0.6), int(bg.height * 0.6))
        )
        bg_base = Image.new(
            "RGBA", (int((bg.width + fg.width) * 0.7), bg.height), (0,) * 4
        )
        fg_base = bg_base.copy()
        bg_base.paste(bg, (0, 0))
        fg_base.paste(fg, (fg_base.width - fg.width, fg_base.height - fg.height))
        return Image.alpha_composite(bg_base, fg_base)
    elif args[0] == "then":
        right = getimg(args[2])
        left = getimg(args[1])
        left = left.resize((int(left.width * right.height / left.height), right.height))
        base0 = Image.new(
            "RGBA", (int((right.width + left.width) * 0.9), right.height), (0,) * 4
        )
        base1 = base0.copy()
        base2 = base0.copy()
        base0.paste(right, (base0.width - right.width, 0))
        base1.paste(left, (0, 0))
        arrow = getimg("arrow")
        arrow = arrow.resize(
            (
                int(arrow.width / arrow.height * right.height * 0.5),
                int(right.height * 0.5),
            )
        )
        base2.paste(
            arrow,
            ((base2.width - arrow.width) // 2, base2.height - arrow.height),
        )
        base1 = Image.alpha_composite(base0, base1)
        return Image.alpha_composite(base1, base2)
    else:
        return getimg(args[0])


def main():
    with open("./src/config.toml") as f:
        config = toml.load(f)
    for key, val in config.items():
        for num, args in val.items():
            img = edit(args.split())
            img.save(f"./dist/{num}_{key}.png")


if __name__ == "__main__":
    main()
