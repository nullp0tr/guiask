from getch import *
import shutil
from gbigchar import *
import gcolors


class TKeys:
    ARROW_UP = '\x1b[A'
    ARROW_DOWN = '\x1b[B'
    ARROW_RIGHT = '\x1b[C'
    ARROW_LEFT = '\x1b[D'
    CTRL_SHIFT_A = '\x1b\x01'
    ENTER_HEX = '\x0D'
    ENTER_CR = '\r'
    ENTER_NL = '\n'
    CTRL_A = '\x01'
    CTRL_B = '\x02'
    CTRL_C = '\x03'
    CTRL_D = '\x04'
    CTRL_E = '\x05'
    CTRL_F = '\x06'
    CTRL_G = '\x07'
    CTRL_H = '\x08'
    CTRL_I = '\x09'
    CTRL_J = '\x0A'
    CTRL_K = '\x0B'
    CTRL_L = '\x0C'
    CTRL_M = '\x0D'
    CTRL_N = '\x0E'
    CTRL_O = '\x0F'
    CTRL_P = '\x10'
    CTRL_Q = '\x11'
    CTRL_R = '\x12'
    CTRL_S = '\x13'
    CTRL_T = '\x14'
    CTRL_U = '\x15'
    CTRL_V = '\x16'
    CTRL_W = '\x17'
    CTRL_X = '\x18'
    CTRL_Y = '\x19'
    CTRL_Z = '\x1A'


# add scrollable attribute
class TerminalDrawable(object):
    def __init__(self):
        self.scrollable = False
        self.input_scrollable = False
        self.color = None
        self.indent = None
        self.prefix = None
        self.fulfilled = False
        self.identifiers = None

    def draw(self, *args, **kwargs):
        pass

    def _headline_indent(self, *args, **kwargs):
        pass

    def addtodrawable(self, *args, **kwargs):
        pass


class TerminalListItem(TerminalDrawable):
    def __init__(self,
                 name,
                 indent=None,
                 color=None,
                 scrollable=True,
                 prefix=None,
                 align_to_center=False,
                 identifiers=None):
        TerminalDrawable.__init__(self)
        self.name = name
        self.saved_name = self.name
        self.scrollable = scrollable
        self.indent = indent
        self.color = color
        self.prefix = prefix
        self.align_to_center = align_to_center
        self.identifiers = identifiers

    def _align_to_center(self, **kwargs):
        columns = kwargs['columns']
        length = len(self.name)
        indent = int((columns - length) / 2)
        self.name = self.saved_name
        self.name = '\033[' + str(indent) + 'C' + self.name

    def draw(self, *args, **kwargs):
        if self.align_to_center:
            self._align_to_center(columns=kwargs['columns'])
        return self.name

    def __str__(self):
        return self.name


class TerminalInputListItem(TerminalDrawable):
    def __init__(self,
                 name,
                 indent=None,
                 color=None,
                 prefix=None,
                 align_to_center=False,
                 identifiers=None,
                 hidden=False):
        TerminalDrawable.__init__(self)
        self.name = name
        self.saved_name = self.name
        self.input = ''
        self.indent = indent
        self.color = color
        self.prefix = prefix
        self.align_to_center = align_to_center
        self.input_scrollable = True
        self.identifiers = identifiers
        self.hidden = hidden

    def draw(self, *args, **kwargs):
        if self.hidden:
            return self.name + '*' * len(self.input)
        return self.name + self.input

    def addtodrawable(self, *args, **kwargs):
        tobeadded = kwargs.get('tobeadded', '')
        esclines = ('\n', '\r', '\t', '\f')
        if tobeadded == '\x7f':
            self.input = self.input[:-1]
        elif tobeadded not in esclines:
            self.input += tobeadded


class TerminalHeadline(TerminalDrawable):
    def __init__(self, headline, font, scale, color=None):
        TerminalDrawable.__init__(self)
        self.saved_headline = buildbigcharfont(
            string=headline, font=font, scale=scale)
        self.headline = self.saved_headline
        self.color = color

    def _headline_indent(self, columns):
        length = len(self.saved_headline.split('\n')[0])
        indent = int((columns - length) / 2)
        self.headline = self.saved_headline
        self.headline = '\033[' + str(indent) + 'C' + self.headline
        self.headline = self.headline.replace('\n',
                                              '\n\033[' + str(indent) + 'C')

    def draw(self, *args, **kwargs):
        columns = kwargs['columns']
        self._headline_indent(columns)
        return self.headline

    def __str__(self):
        return self.headline


class TerminalScreenshot(object):
    def __init__(self, name):
        self.name = name
        self.drawables = []
        self.scrollables = []
        self.input_scrollables = []
        self.input_handler = None
        self.identifiers = {}

    def append_drawable(self, drawable):
        self.drawables += [drawable, ]
        if drawable.scrollable:
            current_index = len(self.drawables) - 1
            self.scrollables.append(current_index)
            self.identifiers[current_index] = drawable.identifiers
        elif drawable.input_scrollable:
            current_index = len(self.drawables) - 1
            self.input_scrollables.append(current_index)
            self.identifiers[current_index] = drawable.identifiers

    def get_identifiers(self, **kwargs):
        identifiers = None
        selected_entry = kwargs.get('selected_entry', None)
        if selected_entry is not None:
            identifiers = self.identifiers[selected_entry]
        return identifiers


class HeadlineListScreenshot(TerminalScreenshot):
    def __init__(self,
                 name,
                 headline,
                 list_entries,
                 font=medium_circle_char_font,
                 scale=1,
                 input_handler=None,
                 color=None):
        TerminalScreenshot.__init__(self, name)
        self.input_handler = input_handler
        self.append_drawable(TerminalHeadline(headline, font, scale, color))
        for list_entry in list_entries:
            scrollable = list_entry.get('scrollable', True)
            prefix = list_entry.get('prefix', None)
            align_to_center = list_entry.get('align_to_center', False)
            identifiers = list_entry.get('ids', None)
            name = list_entry.get('entry', '')
            color = list_entry.get('color', None)
            indent = list_entry.get('indent', None)
            drawable = TerminalListItem(
                name=name,
                color=color,
                indent=indent,
                scrollable=scrollable,
                prefix=prefix,
                identifiers=identifiers,
                align_to_center=align_to_center)
            self.append_drawable(drawable=drawable)


class HeadlineInputListScreenshot(TerminalScreenshot):
    def __init__(self,
                 name,
                 headline,
                 list_entries,
                 font=medium_circle_char_font,
                 scale=1,
                 input_handler=None,
                 color=None):
        TerminalScreenshot.__init__(self, name)
        self.name = name
        self.input_handler = input_handler
        self.append_drawable(TerminalHeadline(headline, font, scale, color))
        for list_entry in list_entries:
            prefix = list_entry.get('prefix', None)
            align_to_center = list_entry.get('align_to_center', False)
            identifiers = list_entry.get('ids', None)
            name = list_entry.get('entry', '')
            color = list_entry.get('color', None)
            indent = list_entry.get('indent', None)
            hidden = list_entry.get('hidden', False)
            drawable = TerminalInputListItem(
                name=name,
                color=color,
                indent=indent,
                prefix=prefix,
                align_to_center=align_to_center,
                identifiers=identifiers,
                hidden=hidden)
            self.append_drawable(drawable=drawable)


class TerminalScreen(object):
    def __init__(self, input_handler=None, terminal_columns=80, terminal_lines=20):

        self.columns, self.lines = shutil.get_terminal_size(
            (terminal_columns, terminal_lines))
        self.screenshot_in_focus = None
        self.screenshots = []
        self.input_handler = input_handler
        self.last_line = self.lines - 2
        self.columns_per_scr = self.columns

    def _clean_values(self):
        pass

    def load(self, screenshot):
        self._clean_values()
        self.screenshot_in_focus = screenshot

    def hotload(self, screenshot):
        self._clean_values()
        scrollables = screenshot.scrollables
        screenshot_ = {'screenshot': screenshot, 'scrollables': scrollables, 'input_scrollables': [],
                       'lines_scrolled': 0, 'printable_size': 0, 'can_scroll_down': False,
                       'highlighted': None}
        self.screenshots += [screenshot_, ]
        self.columns_per_scr = int(self.columns / len(self.screenshots))
        self.screenshot_in_focus = self.screenshots[-1]

    def unload(self):
        self.screenshots.clear()

    def _update_screen_size(self):
        self.columns, self.lines = shutil.get_terminal_size((80, 20))
        self.columns = self.columns
        self.last_line = self.lines - 2
        self.columns_per_scr = self.columns
        if self.screenshots:
            self.columns_per_scr = int(self.columns / len(self.screenshots))

    @staticmethod
    def _clear_screen():
        return '\033c'

    def _cursor_down(self):
        return "\033[" + str(self.lines - 1) + ";3H"

    def _draw_screenshot(self, tbscr, scrindex=0):
        printable = []
        for i, drawable in enumerate(tbscr['screenshot'].drawables):

            color = ''
            indent = 0
            prefix = ''
            if drawable.color is not None:
                color = gcolors.gcolors.get(drawable.color, None)

            if drawable.indent is not None:
                indent = drawable.indent

            if drawable.prefix is not None:
                prefix = drawable.prefix

            if hasattr(drawable, 'align_to_center'):
                if drawable.align_to_center:
                    indent = int((self.columns - len(drawable.draw())) / 2)

            screenshot_is_in_focus = self.screenshot_in_focus['screenshot'] == tbscr['screenshot']

            if drawable.input_scrollable and screenshot_is_in_focus:
                if drawable.fulfilled:
                    if i in tbscr['input_scrollables']:
                        tbscr['input_scrollables'].remove(i)

                else:
                    if i not in tbscr['input_scrollables']:
                        tbscr['input_scrollables'].append(i)
                    if tbscr['input_scrollables'][0] == i:
                        tbscr['highlighted'] = i

                        color = gcolors.gcolors['highlighted']

            if drawable.scrollable and len(tbscr['input_scrollables']) == 0 and screenshot_is_in_focus:
                if i not in self.screenshot_in_focus['scrollables']:
                    self.screenshot_in_focus['scrollables'].append(i)

                # is_highlighted = tbscr['highlighted'] == i
                is_highlighted = self.screenshot_in_focus['highlighted'] == i

                # noting_is_highlighted = tbscr['highlighted'] is None
                noting_is_highlighted = self.screenshot_in_focus['highlighted'] is None

                if (is_highlighted or noting_is_highlighted) and screenshot_is_in_focus:
                    color = gcolors.gcolors['highlighted']
                    # tbscr['highlighted'] = i
                    self.screenshot_in_focus['highlighted'] = i

            scrsplitfix = ("\033[" + str(self.columns_per_scr) + "C")

            if isinstance(drawable, TerminalHeadline):
                headline = drawable.draw(
                    columns=self.columns_per_scr,
                    lines=self.lines)
                lines = headline.split('\n')
                for line_ in lines:
                    line = ' ' * indent + prefix + color + \
                           line_ + gcolors.gcolors['normal']
                    line = scrsplitfix * scrindex + line
                    printable.append(line)
            else:
                line_ = drawable.draw(columns=self.columns, lines=self.lines)
                line_start = ' ' * indent + prefix

                def strindinsert(string, index, char):
                    return string[:index] + char + string[index:]

                j = len(line_start)
                for ii, _ in enumerate(line_):
                    if j >= self.columns_per_scr:
                        line_ = strindinsert(line_, ii, '\n' + scrsplitfix * scrindex)
                        j = 0
                    else:
                        j += 1

                line = line_start + color + line_ + gcolors.gcolors['normal']
                line = scrsplitfix * scrindex + line
                printable.append(line)

        scrcursup = "\033[0;0H"
        scrsplitfix = ("\033[" + str(self.columns_per_scr) + "C")
        new_printable = scrcursup
        lines_scrolled = tbscr['lines_scrolled']

        for iii, line in enumerate(printable[lines_scrolled:]):
            if iii == self.last_line:
                tbscr['can_scroll_down'] = True
                tbscr['printable_size'] = len(printable)
                new_printable += scrsplitfix * scrindex + '.....'
                break
            tbscr['can_scroll_down'] = False
            new_printable += line + '\n'

        return new_printable

    def scrollup(self):
        try:
            index_of_current_scrollable = self.screenshot_in_focus['scrollables'].index(
                self.screenshot_in_focus['highlighted'])
            self.screenshot_in_focus['highlighted'] = self.screenshot_in_focus['scrollables'][
                index_of_current_scrollable - 1]
            no_lines_scrolled = self.screenshot_in_focus['lines_scrolled'] == 0
            is_last_line = self.screenshot_in_focus['scrollables'][-1] == self.screenshot_in_focus['highlighted']
            if no_lines_scrolled and is_last_line:
                self.screenshot_in_focus['lines_scrolled'] = self.screenshot_in_focus['printable_size'] - self.last_line
                self.screenshot_in_focus['lines_scrolled'] += 1
            if self.screenshot_in_focus['lines_scrolled'] > 0 and index_of_current_scrollable + int(
                    (self.lines / 4)) < len(
                    self.screenshot_in_focus['scrollables']):
                self.screenshot_in_focus['lines_scrolled'] -= 1
        except IndexError:
            self.screenshot_in_focus['lines_scrolled'] = self.screenshot_in_focus['scrollables'][-1]
        except ValueError:
            pass

    def scrolldown(self):
        try:
            index_of_current_scrollable = self.screenshot_in_focus['scrollables'].index(
                self.screenshot_in_focus['highlighted'])
            self.screenshot_in_focus['highlighted'] = self.screenshot_in_focus['scrollables'][
                index_of_current_scrollable + 1]
            if self.screenshot_in_focus['can_scroll_down']:
                self.screenshot_in_focus['lines_scrolled'] += 1
        except IndexError:
            self.screenshot_in_focus['highlighted'] = self.screenshot_in_focus['scrollables'][0]
            self.screenshot_in_focus['lines_scrolled'] = 0
        except ValueError:
            pass

    def gorightfocus(self):
        for i, screenshot_ in enumerate(self.screenshots):
            if self.screenshot_in_focus == screenshot_ and i <= len(self.screenshots):
                self.screenshot_in_focus = self.screenshots[i + 1]
                return
            self.screenshot_in_focus = self.screenshots[0]

    def _get_input(self):
        ch = getchar()
        if ch is None:
            return
        if self.input_handler is not None:
            self.input_handler(char=ch)
        ids = self.screenshot_in_focus['screenshot'].get_identifiers(
            selected_entry=self.screenshot_in_focus['highlighted'])

        if self.screenshot_in_focus['screenshot'].input_handler is not None:
            self.screenshot_in_focus['screenshot'].input_handler(
                char=ch, screenshot_name=self.screenshot_in_focus['screenshot'].name, ids=ids,
                screenshot=self.screenshot_in_focus['screenshot'],
                selected_entry=self.screenshot_in_focus['highlighted'],
                screen=self)

    def loop(self):
        while True:
            self._update_screen_size()
            prnta = ''
            for i, tbscr in enumerate(self.screenshots):
                prnt = self._draw_screenshot(tbscr, scrindex=i)
                prnta += prnt
            print(self._clear_screen() + prnta)
            self._get_input()
