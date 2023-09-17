'''This module deals with some common terminal output functions'''

import os
import sys


def clear_lines(lines:int = 1):
    """
    Clears from current line, n lines up.
    * n (default 1) must be a positive integer.
    * setting n to -1 clears the entire terminal.
    """
    if lines > 0:
        for _ in range(lines):
            sys.stdout.write('\x1b[1A' )    # Move cursor up.
            sys.stdout.write('\x1b[2K' )    # Erase line at cursor.
    elif lines < 0:
        # Repeated 2 times to get rid of that annoying scroll buffer.
        # Set to a higher value for smaller terminals
        # NOTE: Higher values results in terminal flickering
        for _ in range(abs(lines)):
            os.system('cls' if os.name == 'nt' else 'clear')


def print_border(width:int = 72, symbol:str = "*") -> None:
    """Prints a 78 char long border for dividing sections"""
    for _ in range(width):
        # \x1b[2k prints "symbol" on the same line.
        sys.stdout.write(f'{symbol}\x1b[2k')
    print("")


def print_columns(list1:list, list2:list) -> None:
    """
    Tabulates and prints a list:
    * list1: The row headings (Length of list determines number of columns)
    * list2: The objects to list
    * width: How many characters wide the table must be.
    """
    make_bold = "\033[1m"  # Start Bold string
    underline = "\033[4m"  # Start Underline
    stop = "\033[0m"  # Stop format
    num_columns = len(list1)
    space = len(str(len(list2)))    # Get space of numbering
    count = 1   # For tracking position in table
    format_2 = "{:2d}"  # Format numbering

    # Determine ratio of column widths by taking the maximum width per column
    ratio_list1 = [len(str(ele)) for ele in list1]
    ratio_list2 = []

    temp = []
    for i in range(0, num_columns):
        for sub_list in list2:
            try:
                temp.append(len(str(sub_list[i])))
            except IndexError:
                temp.append(0)

        ratio_list2.append(max(temp))
        temp.clear()

    ratio = []
    for i, value in enumerate(ratio_list1, 0):
        if value >= ratio_list2[i]:
            ratio.append(value)
        else:
            ratio.append(ratio_list2[i])

    # Print first line (To close table at top)
    print(make_bold, underline)
    print(".   ", end=" ")
    for i in range(num_columns):
        format_1 = "{:<"+ str(ratio[i] + space) + "}"
        print(".",format_1.format(""), end="")
    print(".")
    print("|   ", end=" ")

    # Print Headers (1st row)
    for i in range(num_columns):
        format_1 = "{:<"+ str(ratio[i] + space) + "}"
        print("|",format_1.format(list1[i]), end="")
    print("|")
    print(stop)

    # Print body (Remaining rows)
    clear_lines(1)
    print(underline)
    clear_lines(1)

    for ele in list2:
        # Format line 1 of each row.
        # Calculate space between elements of row 1
        print("|", format_2.format(count), end=" ")
        for i in range(num_columns):
            format_1 = "{:<"+ str(ratio[i] + space) + "}"
            try:
                print("|",format_1.format(ele[i]), end="")
            except IndexError:
                print("|",format_1.format(""), end="")
        print("|")
        count += 1
    print(stop)


def print_header(header:str = "", sub_header:str = "", width:int = 0) -> None:
    """
    Clears and prints a header in the terminal.
    The message argument is optional.
    """
    clear_lines(-1)
    print_border(width)
    print(header)
    print(sub_header)
    print_border(width)


def format_rands(self):
    """Format value into South African currency format"""
    self = f"R{self:,.2f}"
    self = self.replace(","," ")
    self = self.replace(".",",")
    return self


def format_cost(self):
    """
    Format value into a format congruent with that in 'inventory.txt'
    """
    self = f"{self:,.2f}"
    self = self.replace(",","")
    return self