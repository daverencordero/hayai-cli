class Section(object):
    def __init__(self, title: str, level: int, **kwargs):
        self.title = title  # Representative String on Print
        self.level = level  # Defining the depth of section from root (root = 0)
        self.sub_sections = []  # Sub-sections of the menu
        self.method = None  # Method ran on menu select

        # Parses the Kwargs values
        if 'sub_sections' in kwargs:
            self.add_sub_sections(*kwargs['sub_sections'])
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        if 'method' in kwargs:
            self.method: classmethod = kwargs['method']

    # Gets parent section
    def prev(self):
        return self.parent

    # Gets a particular section descendant
    def next(self, index: int):
        return self.sub_sections[index]

    # Sets method ran on select
    def set_method(self, method):
        self.method = method

    # Adds empty sections to the sub_sections list (note: empty section = no method)
    def add_sub_sections(self, *args):
        for menu_title in args:
            self.sub_sections.append(Section(menu_title, self.level + 1, parent=self))

    # Adds a sub section
    def add_sub_section(self, menu_title, **kwargs):
        kwargs['parent'] = self
        menu = Section(menu_title, self.level + 1, **kwargs)
        self.sub_sections.append(menu)

    # Prints all sub sections
    def print(self, **kwargs):
        for index, section in enumerate(self.sub_sections):
            text_format = '> {}'
            if 'start_index' in kwargs:
                index += kwargs['start_index']
            if 'format' in kwargs:
                text_format = kwargs['format']
                text_format = text_format.replace("#", str(index))
            print(text_format.format(section.title))

    # Runs section method
    def run(self):
        if self.method is not None:
            self.method()


class HayaiMenu:  # Class that handles the entire menu
    def __init__(self, menu_title, **kwargs):
        self.root = Section(menu_title, 0)  # Stores root node
        self.current = self.root

        # Stylizing Variables
        self.separator_char = "="
        self.separator_width = 50

        # Parses the Kwargs Values
        if 'separator_char' in kwargs:
            self.char = kwargs['separator_char']
        if 'separator_width' in kwargs:
            self.separator_width = kwargs['separator_width']

    # Gets specific section via title and level
    def get_section(self, title: str, level: int):
        focus = self.root
        section = None
        while focus.sub_sections:
            for sub_section in focus.sub_sections:
                if sub_section.title == title and sub_section.level == level:
                    section = sub_section
                elif section is not None:
                    section = self.get_section(title, level)
                else:
                    break
        return section

    def set_current_prev(self, index: int):
        self.current = self.root.prev()

    def set_current_next(self, index: int):
        self.current = self.root.next(index)

    def set_current(self, title: str, level: int):
        self.current = self.get_section(title, level)

    def get_current(self):
        return self.current

    def get_root(self):
        return self.root

    def print(self, **kwargs):
        Bcolors.print(self.current.title.center(self.separator_width, self.separator_char), Bcolors.OKGREEN)
        self.current.print(**kwargs)

    def run(self):
        self.current.run()


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print(text: str, color: str):
        print(color + text + Bcolors.HEADER)
