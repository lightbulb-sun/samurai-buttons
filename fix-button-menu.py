#!/usr/bin/python3

ROM_INPUT  = 'samuraishodown.sfc'
ROM_OUTPUT = 'options.sfc'

CHAR_A     = 0x2100
CHAR_DASH  = 0x213e
CHAR_SPACE = 0x01ff
CHAR_DOT   = 0x213c

BUTTON_TEXT_OFFSET = 0x1f370e
NEW_BUTTON_TEXT_OFFSET = 0x1ff000

POINTER_P1 = 0x1f34fb
POINTER_P2 = 0x1f35df

LINE_LENGTH = 10
LINE_DATA_LENGTH = 0x30

LINES = (
        'L-SLASH ..',
        'M-SLASH ..',
        'L-KICK  ..',
        'M-KICK  ..',
        'H-SLASH ..',
        'H-KICK  ..',
        )


def read_rom(filename):
    with open(filename, 'rb') as inf:
        return bytearray(inf.read())


def write_rom(rom, filename):
    with open(filename, 'wb') as outf:
        outf.write(rom)


def write_word(rom, offset, word):
    rom[offset+0] = word & 0xff
    rom[offset+1] = (word >> 8) & 0xff


def char_to_tile_number(char):
    if ord('A') <= ord(char) <= ord('Z'):
        return CHAR_A + 2*(ord(char)-ord('A'))
    if char == '-':
        return CHAR_DASH
    if char == '.':
        return CHAR_DOT
    if char == ' ':
        return CHAR_SPACE
    raise Exception(f'Unknown character: {char}')


def change_tiles(rom, offset, s):
    for n, char in enumerate(s):
        tile = char_to_tile_number(char)
        write_word(rom, offset+2*n, tile)
        write_word(rom, offset+2*LINE_LENGTH+2*n, tile+1)


def change_line(rom, num, s):
    offset = BUTTON_TEXT_OFFSET + LINE_DATA_LENGTH*num + 8
    change_tiles(rom, offset, s)


def change_extra_line(rom, s):
    offset = NEW_BUTTON_TEXT_OFFSET + 8
    change_tiles(rom, offset, s)


def copy_line(rom):
    for i in range(LINE_DATA_LENGTH):
        rom[NEW_BUTTON_TEXT_OFFSET+i] = rom[BUTTON_TEXT_OFFSET+4*LINE_DATA_LENGTH+i]


def patch_pointers(rom):
    write_word(rom, POINTER_P1, NEW_BUTTON_TEXT_OFFSET & 0xffff)
    write_word(rom, POINTER_P2, NEW_BUTTON_TEXT_OFFSET & 0xffff)


def main():
    rom = read_rom(ROM_INPUT)
    for n, line in enumerate(LINES[:-1]):
        change_line(rom, n, line)
    copy_line(rom)
    change_extra_line(rom, LINES[-1])
    patch_pointers(rom)
    write_rom(rom, ROM_OUTPUT)


if __name__ == '__main__':
    main()
