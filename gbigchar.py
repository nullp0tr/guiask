medium_circle_char_font = {
    'A': '●●●●●'
         '●   ●'
         '●●●●●'
         '●   ●'
         '●   ●',
    'B': '●●●● '
         '●   ●'
         '●●●● '
         '●   ●'
         '●●●● ',
    'C': '●●●●●'
         '●    '
         '●    '
         '●    '
         '●●●●●',
    'D': '●●●● '
         '●   ●'
         '●   ●'
         '●   ●'
         '●●●● ',
    'E': '●●●●●'
         '●    '
         '●●●●●'
         '●    '
         '●●●●●',
    'F': '●●●●●'
         '●    '
         '●●●●●'
         '●    '
         '●    ',
    'G': '●●●●●'
         '●    '
         '●  ●●'
         '●   ●'
         '●●●●●',
    'H': '●   ●'
         '●   ●'
         '●●●●●'
         '●   ●'
         '●   ●',
    'I': '●●●●●'
         '  ●  '
         '  ●  '
         '  ●  '
         '●●●●●',
    'K': '●   ●'
         '●  ● '
         '●●●  '
         '●  ● '
         '●   ●',
    'J': '●●●●●'
         '   ● '
         '   ● '
         '●  ● '
         '●●●● ',
    'L': '●    '
         '●    '
         '●    '
         '●    '
         '●●●●●',
    'M': '●   ●'
         '●● ●●'
         '● ● ●'
         '●   ●'
         '●   ●',
    'N': '●   ●'
         '●●  ●'
         '● ● ●'
         '●  ●●'
         '●   ●',
    'O': ' ●●● '
         '●   ●'
         '●   ●'
         '●   ●'
         ' ●●● ',
    'P': '●●●● '
         '●   ●'
         '●●●● '
         '●    '
         '●    ',
    'Q': ' ●●● '
         '●   ●'
         '● ● ●'
         '●  ●●'
         ' ●●●●',
    'R': '●●●● '
         '●   ●'
         '●●●● '
         '●   ●'
         '●   ●',
    'S': '●●●●●'
         '●    '
         '●●●●●'
         '    ●'
         '●●●●●',
    'T': '●●●●●'
         '  ●  '
         '  ●  '
         '  ●  '
         '  ●  ',
    'U': '●   ●'
         '●   ●'
         '●   ●'
         '●   ●'
         ' ●●● ',
    'V': '●   ●'
         '●   ●'
         '●   ●'
         ' ● ● '
         '  ●  ',
    'W': '●   ●'
         '●   ●'
         '● ● ●'
         '●● ●●'
         '●   ●',
    'X': '●   ●'
         ' ● ● '
         '  ●  '
         ' ● ● '
         '●   ●',
    'Y': '●   ●'
         ' ● ● '
         '  ●  '
         '  ●  '
         '  ●  ',
    'Z': '●●●●●'
         '   ● '
         '  ●  '
         ' ●   '
         '●●●●●',
    ' ': '     '
         '     '
         '     '
         '     '
         '     ',
    'WIDTH': 5,
    'HEIGHT': 5,
    'SYMBOL': '●',
}
big_square_char_font = {
    'A': '■■■■■■■'
         '■     ■'
         '■     ■'
         '■■■■■■■'
         '■     ■'
         '■     ■'
         '■     ■',
    'B': '■■■■■■ '
         '■     ■'
         '■     ■'
         '■■■■■■ '
         '■     ■'
         '■     ■'
         '■■■■■■ ',
    'C': '■■■■■■■'
         '■      '
         '■      '
         '■      '
         '■      '
         '■      '
         '■■■■■■■',
    'D': '■■■■■■ '
         '■     ■'
         '■     ■'
         '■     ■'
         '■     ■'
         '■     ■'
         '■■■■■■ ',
    'G': '■■■■■■■'
         '■      '
         '■      '
         '■   ■■■'
         '■     ■'
         '■     ■'
         '■■■■■■■',
    'S': '■■■■■■■'
         '■      '
         '■      '
         '■■■■■■■'
         '      ■'
         '      ■'
         '■■■■■■■',
    'K': '■    ■■'
         '■   ■■ '
         '■  ■■  '
         '■■■    '
         '■  ■■  '
         '■   ■■ '
         '■    ■■',
    ' ': '       '
         '       '
         '       '
         '       '
         '       '
         '       '
         '       ',
    'WIDTH': 7,
    'HEIGHT': 7,
    'SYMBOL': '■'
}


def buildbigcharfont(string, font, scale=2):
    font_width = font['WIDTH']
    font_height = font['HEIGHT']

    def string_to_big_char_string(string_):
        big_char_list = []
        for c in string_:
            try:
                if c == '\n':
                    big_char_list.append(c)
                else:
                    big_char_list.append(font[c.upper()])
            except KeyError:
                raise TypeError('Character not supported')

        return big_char_list

    char_list = string_to_big_char_string(string)
    big_char_string = ''
    for index in range(font_height):
        for _ in range(scale):
            for char in char_list:
                char_line = char[index * font_width:index * font_width + font_width]
                if scale > 1:
                    font_symbol = font['SYMBOL']

                    def rreplace(string_, new_, old_, count_):
                        return new_.join(string_.rsplit(old_, count_))

                    char_line = (' ' * (scale - 1)) + char_line + (' ' * (scale - 1))
                    new = font_symbol * scale
                    char_line = rreplace(char_line, str(new), font_symbol + ' ', 1)
                    char_line = char_line.replace(' ' + font_symbol,
                                                  font_symbol * scale, 1)

                big_char_string += char_line + '  '

            big_char_string += '\n'

    return big_char_string
