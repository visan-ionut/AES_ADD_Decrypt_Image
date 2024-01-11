from collections import Counter

from PIL import Image


def get_image_size(header: bytes) -> tuple[int, int]:
    dheader: str = header.decode("utf-8")

    # ignore comments as well
    lines = [line for line in dheader.split("\n") if not line.startswith("#")]

    # PPM format:
    #   - line 1 -> P6
    #   - line 2 -> width height
    #   - line 3 -> maximum pixel intensity
    width, height = map(int, lines[1].split())

    return width, height


def break_encryption(
    ecb_blocks: list[int], w: int, h: int, background: int
) -> Image.Image:
    im = Image.new("RGB", (w, h))
    data = []
    for b in ecb_blocks:
        if b == background:
            data += [(0, 0, 0)]
        else:
            data += [(255, 255, 255)]
    im.putdata(data)
    return im


def decrypt_image(enc_filename: str) -> Image.Image:
    with open(enc_filename, "rb") as file:
        header, data = parse_header_ppm(file.read())

    width, height = get_image_size(header)

    ########## SOLUȚIA AICI ##########
    # TODO 1: Inversați pasul ADD din AES-ADD.

    # Function to perform inverse addition modulo UMAX
    def inv_add(block1, block2):
        return (block1 - block2) % UMAX

    # Divide the data into blocks of size BLOCK_SIZE
    blocks = [data[i * BLOCK_SIZE : (i + 1) * BLOCK_SIZE] for i in range(len(data) // BLOCK_SIZE)]

    # Convert the first block to a numerical representation and store it in ecb_blocks
    ecb_blocks = [bytes_to_num(blocks[0])]

    # Iterate over pairs of consecutive blocks, apply inverse addition, and add the result to ecb_blocks
    ecb_blocks.extend(inv_add(bytes_to_num(curr), bytes_to_num(prev)) for prev, curr in zip(blocks, blocks[1:]))

    # TODO 2: Determinati block-ul din cipertext-ul AES-ECB care se repetă de
    # cele mai multe ori. Acesta va fi culoarea de background, in imaginea
    # alb-negru pe care o veti obtine.

    # Find the most common numerical representation in ecb_blocks using Counter
    # and store it as the 'background' value
    background = Counter(ecb_blocks).most_common(1)[0][0]
    ##################################

    # Using the scale factor, we make the image more readable. Also, the image
    # will repeat `scale_factor` times.
    scale_factor = 2
    img = break_encryption(
        ecb_blocks,
        round(scale_factor * 3 * width / 16),
        height // scale_factor + 1,
        background,
    )
    return img


im = decrypt_image("my_precious.enc.ppm")
im