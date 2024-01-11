=====================
AES ADD Decrypt Image
=====================

The decrypt_image function processes an encrypted image
using the AES-ADD variant. It parses the image header,
reverses the AES-ADD encryption, determines the background
color, and creates a new image by mapping encrypted blocks
to pixels. The resulting decrypted image is displayed,
revealing the hidden content.

Note: You have to parse an encrypted image.
