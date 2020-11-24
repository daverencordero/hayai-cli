class Section(object):
    def __init__(self, title: str, level: int, parent, **kwargs):
        self.title = title  # Representative String on Print
        self.level = level  # Defining the depth of section from root (root = 0)
        self.parent = parent
        self.sub_sections = []  # Sub-sections of the menu
        self.method = None  # Method ran on menu select

        # Parses the Kwargs values
        if 'sub_sections' in kwargs:
            self.add_empty_sub_sections(*kwargs['sub_sections'])
        if 'method' in kwargs:
            self.method = kwargs['method']
        if 'is_back' in kwargs:
            if kwargs['is_back']:
                self.method = self.prev

    # Gets parent section
    def prev(self):
        return self.parent

    # Gets a particular section descendant
    def next(self, index: int):
        if self.sub_sections:
            return self.sub_sections[index]
        return self

    # Sets method ran on select
    def set_method(self, method):
        self.method = method

    # Adds empty sections to the sub_sections list (note: empty section = no method)
    def add_empty_sub_sections(self, *args):
        for menu_title in args:
            self.sub_sections.append(Section(menu_title, self.level + 1, self))

    # Adds a sub section from a str title
    def add_sub_section_from_title(self, menu_title, **kwargs):
        menu = Section(menu_title, self.level + 1, self, **kwargs)
        self.sub_sections.append(menu)

    # Gets specific section via title and level
    def get_section(self, title: str, level: int):
        focus = self
        section = None
        for sub_section in focus.sub_sections:
            if sub_section.level > level:
                break
            elif section is not None:
                break
            elif sub_section.title == title and sub_section.level == level:
                section = sub_section
                break
            else:
                section = sub_section.get_section(title, level)
        return section

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
        self.root = Section(menu_title, 0, None)  # Stores root node
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
    def get_section(self, title: str, level: int) -> Section:
        return self.root.get_section(title, level)

    def on_section(self, title: str, level: int) -> bool:
        return self.current == self.get_section(title, level)

    def set_current_prev(self):
        self.current = self.root.prev()

    def set_current_next(self, index: int):
        self.current = self.current.next(index)

    def set_current_with_section(self, section: Section):
        self.current = section

    def set_current(self, title: str, level: int):
        self.current = self.get_section(title, level)

    def get_current(self) -> Section:
        return self.current

    def get_root(self) -> Section:
        return self.root

    def print(self, **kwargs):
        Bcolors.print(self.current.title.center(self.separator_width, self.separator_char), Bcolors.OKGREEN)
        self.current.print(**kwargs)
        Bcolors.print(''.center(self.separator_width, self.separator_char), Bcolors.OKGREEN)

    def select(self):
        self.print()
        user_input = input(': ')
        for section in self.current.sub_sections:
            if user_input.lower() in section.title.lower():
                self.set_current_with_section(section)
                self.current.run()

    def run(self):
        self.current.run()

    @staticmethod
    def make_menu_from_tree(menu_tree: dict, **kwargs):
        first_key = list(menu_tree.keys())[0]
        menu = HayaiMenu(list(menu_tree.keys())[0], **kwargs)
        HayaiMenu.get_section_from_tree(menu.get_root(), menu_tree[first_key]['sub_sections'])
        return menu

    @staticmethod
    def get_section_from_tree(parent: Section, menu_tree: dict):
        for section, options in menu_tree.items():
            method = None
            is_back = False
            if 'method' in options:
                method = options['method']
            if 'is_back' in options:
                is_back = options['is_back']

            parent.add_sub_section_from_title(section, method=method, is_back=is_back)
            if 'sub_sections' in options:
                HayaiMenu.get_section_from_tree(parent.get_section(section, parent.level+1),
                                                menu_tree[section]['sub_sections'])


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
