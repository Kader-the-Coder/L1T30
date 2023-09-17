'''
This algorithm manages the inventory of shoes.
'''
#=============================Comments=================================
# Intentional Deviations from Task instruction:

# view_all - This function will iterate over the shoe list and print the
# details of the shoes returned from the __str__ function. (Optional:
# you can organize your data in a table format by using Python’s
# tabulate module.)

# My function does not print from _str__ function but rather from another
# method "get_list_atr" which returns a list of attributes for convenience.
# Also, I could not get tabulate module to work so resorted to making
# my own.

# re_stock - This function will find the shoe object with the lowest
# quantity, which are the shoes that need to be re-stocked. Ask the
# user if they want to add this quantity of shoes and then update it.
# This quantity should be updated on the file for this shoe.

# This instruction does not makes sense as it is not normally the lowest
# quantity that gets restocked, but rather all quantities that falls
# under a threshold. I took this into consideration and applied getting
# the lowest quantity if a summary section in the event that is what was
# being tested

# Apologies for the inconvenience.

# pylint: disable=unnecessary-lambda

#=====================Importing Modules/Libraries======================

import os
import sys
from display import (clear_lines,
                     print_columns, print_header,
                     format_rands, format_cost)

#========================Defining 'Constants'==========================

PROGRAM_NAME = "\033[1mNIKE SHOE INVENTORY\033[0m"
PROGRAM_SLOGAN = "All of the shoes in one place!"
DIRECTORY = os.path.dirname(__file__)
INVENTORY_TXT = os.path.join(DIRECTORY, "inventory.txt")

WIDTH = 100 # Width of lines for print header function
THRESHOLD_RE_STOCK = 5 # The min. quantity for an item to be restocked.
THRESHOLD_ON_SALE = 50 # The max. quantity for an item to be on sale.

#=========================Defining Classes=============================


class Shoe:
    """
    A class representing a shoe.

    Attributes:
        country: Where the shoes was manufactured.
        code: The shoe reference number.
        product: The brand of the shoe.
        cost: The price of the shoe.
        quantity: How much of the is in stock.
    """

    def __init__(self, country:str,
                 code:str,product:str,
                 cost:float,
                 quantity:int):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity


    def get_cost(self) -> float:
        """Returns the cost of the shoe in rand format."""
        cost = format_rands(self.cost)
        return f"{self.product} ({self.code}) costs {cost}."


    def get_quantity(self) -> int:
        """Returns the quantity of the shoe."""
        return (f"{self.product} ({self.code}) "
                f"has a stock of {self.quantity}.")


    def get_total_value(self) -> int:
        """Returns the total value of the shoe."""
        total_value = format_rands(self.cost * self.quantity)
        return (f"{self.product} ({self.code}) "
                f"has a total value of {total_value}.")


    def get_list_attr(self) -> list:
        """Returns a list of all attribute values"""
        return [self.country,
                self.code,
                self.product,
                format_rands(self.cost),
                self.quantity]


    def __str__(self):
        return (f"{self.country},"
                f"{self.code},"
                f"{self.product},"
                f"{self.cost},"
                f"{self.quantity}")


    def __repr__(self):
        return ("Shoe("
                f"'{self.country}', "
                f"'{self.code}', "
                f"'{self.product}', "
                f"'{self.cost}', "
                f"'{self.quantity}')")


#=========================Initializing Lists===========================
#The list will be used to store a list of objects of shoes.
shoe_list = []

#=========================Defining Functions===========================


def read_shoes_data():
    """
    Populates 'shoe_list' with 'Shoe' objects from 'inventory.txt'.
    """
    # Ensure that "shoe_list" is empty to avoid duplicates.
    shoe_list.clear()
    try:
        with open(INVENTORY_TXT, "r", encoding="utf-8-sig") as file:
            next(file)  # Skips first line
            for lines in file:
                # Format each line before importing to 'shoe_list'.
                temp = lines.strip()
                temp = lines.split(",")
                # Import data to 'shoe_list'
                shoe_list.append(Shoe(temp[0],
                                    temp[1],
                                    temp[2],
                                    float(temp[3]),
                                    int(temp[4].replace("\n", ""))))
    except FileNotFoundError:
        # If file is missing, create new one or exit program based on
        # user decision.
        print("\"inventory.txt\" is missing from your working directory.")
        option = input("Create empty file?\n"
                       "Input either Yes or No.\n"
                       "Choosing No will terminate the program.\n: ")
        if option[0].lower() == "y":
            # Creates empty "inventory.txt" file
            with open(INVENTORY_TXT, "w", encoding="utf-8-sig") as file:
                file.write("Country,Code,Product,Cost,Quantity")
        else:
            # Exit program.
            print("\nProgram will now terminate.")
            print("See you again soon!\n")
            sys.exit()

    except IndexError:
        # If "inventory.txt" file is corrupted (Hence the indexing error),
        # attempt to recover file or exit program based on user decision.
        print("\"inventory.txt\" has been corrupted.\n")
        print("Attempt to recover data? Input either Yes or No.\n"
              "Choosing No will terminate the program.\n"
              "WARNING:RECOVERY IS TOTALLY FAKE AND WILL DELETE ALL DATA "
              "AFTER THE CORRUPT LINE IN FILE!!!"
              "\n: ")
        option = input()
        if option[0].lower() == "y":
            # Recover "inventory.txt" file.
            # NOTE: Recovery deletes all data after the corrupt line in txt file.
            update_shoes_data()
        else:
            # Exit program.
            print("\nProgram will now terminate.")
            print("See you again soon!\n")
            sys.exit()


def update_shoes_data():
    """
    Updates the 'inventory.txt' with data in 'shoe_list' per line
    """
    with open(INVENTORY_TXT, "w", encoding="utf-8-sig") as file:
        temp = "\n".join(str(shoe) for shoe in shoe_list)
        file.write("Country,Code,Product,Cost,Quantity\n")
        file.write(temp)


def capture_shoes_data():
    '''
    Adds a user-input defined shoe (as object) to 'shoe_list'
    '''

    def input_empty(message:str):
        """Returns user input if it is not empty"""
        while True:
            temp = input(message)
            temp = temp.strip()
            temp = temp.lower()
            if temp != "":
                return temp
            print("You did not input anything.")
            input("Press Enter to try again.")
            clear_lines(3)


    def input_text(message:str, input_type:str):
        """Returns user input if input is within 4 to 25 characters"""
        while True:
            temp = input_empty(message)
            if 4 <= len(temp) <= 25:
                temp = temp.title()
                clear_lines(1)
                print(message, temp, sep="")
                return temp
            print(f"Please ensure that the {input_type} "
                  "is from 4 to 25 characters long.")
            input("Press Enter to try again.")
            clear_lines(3)


    def input_code(message:str):
        """
        Returns user input if it is 5 digits.

        ASSUMPTION: A manager working on the program will know how much
        digits the code must be.
        """
        while True:
            temp = input_empty(message)
            try:
                # Check if input is positive and consists of 5 digits.
                if int(temp) < 0 or len(temp) != 5:
                    raise ValueError
            except ValueError:
                print(f"SKU{temp} is not a valid product code. "
                      "Please ensure that your code has 5 digits.")
                input("Press Enter to try again.")
                clear_lines(3)
                continue
            # Add the default letters to code
            temp = "SKU" + temp
            # Check if code is unique (If not, request re-input).
            temp_list = [shoe.code for shoe in shoe_list]
            if temp in temp_list:
                print(f"{temp} already exists. "
                      "Please ensure that your code is unique.")
                input("Press Enter to try again.")
                clear_lines(3)
                continue

            clear_lines(1)
            # "temp[3:]"" prevents printing SKU twice as its already
            # present in "message".
            print(message, temp[3:], sep="")
            return temp


    def input_cost(message:str):
        """
        Returns user input in rands using the "format_rands" function
        if input is a valid cost.
        """
        while True:
            temp = input_empty(message)
            try:
                # Format input before converting to float.
                temp = temp.replace(" ", "")
                temp = temp.replace(",", ".")
                temp = float(temp)
                clear_lines(1)
                print(message[:-1], format_rands(temp), sep="")
                return temp
            except ValueError:
                print(f"{temp} is not a valid amount.")
                input("Press Enter to try again.")
                clear_lines(3)
                continue


    # Request shoe details.
    country = input_text("Country: ", "country")
    code = input_code("   Code: SKU")
    product = input_text("  Brand: ", "product name")
    cost = format_cost(input_cost("   Cost: R"))
    # Create Shoe object, setting quantity to 0.
    shoe_list.append(Shoe(country, code, product, cost, 0))
    update_shoes_data()
    read_shoes_data()    # Called to ensure Shoe is correctly updated.

    # Request user to input quantity.
    re_stock(code)
    print("\nShoe successfully captured!.")
    input("Press ENTER to return to main menu.")


def sort_shoes_data(attr:str | None = None,
                    other:bool = False,
                    reverse:bool = True) -> None:
    """
    Sorts 'shoe_list' by specified attribute. I.e.:

    * attr: "country", "code", "product", "cost" or "quantity"
    * other (Default False): sorts by total value when set to true.
    * reverse (Default True): If list should be reversed when sorted again.
    """
    if other:
        if reverse:
            # Determine if shoe_list was already sorted, reversing if true.
            reverse = (shoe_list == sorted(shoe_list,
                                           key=lambda shoe: value_per_item(shoe)))
        # If shoe_list must not be reversed.
        shoe_list.sort(key=lambda shoe:  value_per_item(shoe),reverse=reverse)
    else:
        if reverse:
            # Determine if shoe_list was already sorted, reversing if true.
            reverse = (shoe_list == sorted(shoe_list,
                                           key=lambda shoe: getattr(shoe, attr)))
        # If shoe_list must not be reversed.
        shoe_list.sort(key=lambda shoe: getattr(shoe, attr),reverse=reverse)


def search_shoes_data(attr:str, value:str):
    '''
     Returns a list of all shoes whose specified attribute matches the
     specified value.
    '''
    temp_list = [shoe for shoe in shoe_list if getattr(shoe, attr).lower() == value.lower()]
    return temp_list


def view_shoes(list_to_view:list = None,
               menu_options:list = None,
               enable_sorting:bool = True) -> (str | None):
    '''
    Prints the details of all Shoe objects in given list.

    * list_to_view: List of Shoe objects that must be printed
        (If set to None, the function will print shoe_list)
    * menu_options: If any additional menu option must be added.
        (If set to None, return to main menu will be displayed)
    * enable_sorting: If the option to sort table must be displayed.
    '''
    # Set default list to "shoe_list"
    if list_to_view is None:
        list_to_view = shoe_list

    # Set default menu option
    if menu_options is None:
        menu_options = ["1 - Return to previous menu"]


    def print_list():
        """Prints list_to_view using the "print_columns" function"""
        temp = []
        # Format and create list for use in "print_columns" function:
        for i, shoe in enumerate(list_to_view):
            temp.append(shoe.get_list_attr())
            temp[i].append(format_rands(value_per_item(shoe)))
        print_columns(["Country", "Code", "Product", "Cost", "Quantity", "Total"],
                      temp)


    def print_options():
        """Enables the use of additional menu options and table sorting"""
        while True:
            if enable_sorting:
                # Create list of ways to sort table.
                print("To sort table, type in the column header you would",
                      "wish to sort by.\n")
                temp_list = ["country", "code", "product", "cost", "quantity", "total"]
            else:
                temp_list = []

            print("What would you like to do?")
            # Print additional menu options and determine user input.
            for i, option in enumerate(menu_options, 1):
                print(option)
                temp_list.append(str(i))
            user_input = input_valid(": ", temp_list)

            # Sorts table if user chose to do so.
            if user_input.lower() in ["country", "code", "product", "cost", "quantity"]:
                sort_shoes_data(user_input.lower())
                return None
            elif user_input.lower() == "total":
                sort_shoes_data(other=True)
                return None
            return user_input


    print_list()
    return print_options()


def re_stock(code:str | None = None):
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.

    * code (Default None): Specify which shoe to restock. If set to none,
        only shoes eligible to be restocked will be displayed
    
    Returns '2' is user requests to exit to main menu
    '''
    option = "0"
    if code is None:
        # Check and print all shoes that are eligible to be restocked
        sort_shoes_data("quantity")
        # Shoes that are eligible are shoes whose quantity is less than
        # the THRESHOLD_RE_STOCK constant.
        temp_list = [shoe for shoe in shoe_list if shoe.quantity <= THRESHOLD_RE_STOCK]
        if len(temp_list) > 0:
            option = view_shoes(temp_list,
                                ["1 - Restock shoe.",
                                "2 - Return to main menu"],
                                False)
        else:
            print("\nThere are no shoes that needs to be restocked.")
            input("Press enter to return to main menu.")
            option ="2"
    else:
        # Proceed to next block if a custom shoe code has been provided.
        option = "1"

    if option == "1":
        if code is None:
            clear_lines(4)
            # Request user to input code of shoe that needs to be restocked
            print("Enter the code of the shoe to be restocked.")
            code = input_valid(": ",[shoe.code for shoe in temp_list], True)
            clear_lines(2)

        # Determine is code is valid.
        shoe = [shoe for shoe in shoe_list if shoe.code == code]
        print(f"\nPlease enter the quantity for \033[1m{code}\033[0m.")
        while True:
            try:
                # Request new value for quantity of shoe
                new_quantity = int(input(": "))
                if new_quantity >= 0:
                    break
                raise ValueError
            except ValueError:
                input("Please input a positive integer value.\n"
                    "Press ENTER to try again.")
                clear_lines(3)
        # Restock shoe
        shoe[0].quantity = new_quantity
        update_shoes_data()
        return None

    if option == "2":
        return "2"

    return None


def value_per_item(shoe:object):
    '''
    This function will calculate the total value of a given shoe.
    '''
    return shoe.cost * shoe.quantity


def view_shoes_sale():
    '''
    Prints shoes that are on sale
    '''
    sort_shoes_data("quantity")
    # Create list of shoes that are eligible to be on sale.
    # Shoes that are eligible are shoes whose quantity is greater
    # than the THRESHOLD_ON_SALE constant.
    temp_list = [shoe for shoe in shoe_list if shoe.quantity >= THRESHOLD_ON_SALE]
    if len(temp_list) > 0:
        view_shoes(temp_list, enable_sorting=False)
    else:
        print("\nThere are no shoes on sale.")
        input("Press ENTER to return to main menu.")


def input_valid(print_message:str,
                expected_input:list,
                case_sensitive:bool = False) -> str:
    """
    Returns user input if user input input matches expected input.

    * print_message: The message to display to user for input.
    * expected_input: A list of valid inputs (As strings).
    * case_sensitive (Default False): If user input is case sensitive.
    """
    while True:
        user_input = input(print_message)
        user_input = user_input if case_sensitive else user_input.lower()
        if user_input in expected_input:
            return user_input

        print(f"\"{user_input}\" is not a valid option.")
        input("Press ENTER to try again.")
        clear_lines(3)


def view_shoe_summary() -> None:
    """
    Prints a summary of shoe data.
    """
    print()

    def summary(message:str, attr:str, highest:bool) -> None:
        """
        Prints the shoes with the highest/lowest value of a given attribute

        * message: The message to display above information
        * message: The attribute to check ("cost", "quantity" or "other").
        * highest: True to show highest, else False to show lowest
        """
        if attr != "other":
            sort_shoes_data(attr,reverse=False)
        else:
            sort_shoes_data(other=True,reverse=False)

        print(message)
        # Determine index to look at (First or last)
        i = -1 if highest else 0

        if attr == "cost":
            # Final "if" statement is in the case of duplicates.
            temp_shoe_list = [shoe for shoe in shoe_list
                              if shoe.cost == shoe_list[i].cost]
            for shoe in temp_shoe_list:
                print("*", shoe.get_cost())

        elif attr == "quantity":
            # Final "if" statement is in the case of duplicates.
            temp_shoe_list = [shoe for shoe in shoe_list
                              if shoe.quantity == shoe_list[i].quantity]
            for shoe in temp_shoe_list:
                print("*", shoe.get_quantity())

        elif attr == "other":
            # Final "if" statement is in the case of duplicates.
            temp_shoe_list = [shoe for shoe in shoe_list
                              if value_per_item(shoe) == value_per_item(shoe_list[i])]
            for shoe in temp_shoe_list:
                print("*", shoe.get_total_value())

        print()

    # Print summary.
    summary("\033[1mHighest cost:\033[0m","cost", True)
    summary("\033[1mLowest cost:\033[0m","cost", False)
    summary("\033[1mGreatest quantity:\033[0m","quantity", True)
    summary("\033[1mLowest quantity:\033[0m","quantity", False)
    summary("\033[1mHighest Total Value:\033[0m","other", True)
    summary("\033[1mLowest Total Value:\033[0m","other", False)

    # Print additional summary info.
    print("The total number of all shoes in stock amounts to:")
    total_stock = sum(shoe.quantity for shoe in shoe_list)
    print("\033[1m", total_stock, "shoes", "\033[0m\n")

    print("The total value of all shoes in stock amounts to:")
    total_value = format_rands(sum(value_per_item(shoe) for shoe in shoe_list))
    print("\033[1m", total_value, "\033[0m\n")

#==============================Main Menu===============================
# Create a menu that executes each function above.
# This menu should be inside the while loop. Be creative!
while True:
    print_header(PROGRAM_NAME, PROGRAM_SLOGAN, WIDTH)
    read_shoes_data() # Called in while loop to check for any file corruption
    print_header(PROGRAM_NAME, PROGRAM_SLOGAN, WIDTH)
    # If shoe_list contains data, enable all options
    if len(shoe_list) > 0:
        print(f'''
1 - View all shoes.
2 - View a specific shoe.
3 - View shoes on sale.
4 - View shoes that needs to be restocked.
5 - View summary.
6 - Capture a new shoe
7 - Exit {PROGRAM_NAME} program.
            ''')
        menu = input_valid(": ", ["1", "2", "3", "4", "5", "6", "7"])
    else:
        # Disable options if shoe_list is empty to avoid runtime errors.
        print(f'''
1 - Option disabled - No shoes in inventory.
2 - Option disabled - No shoes in inventory.
3 - Option disabled - No shoes in inventory.
4 - Option disabled - No shoes in inventory.
5 - Option disabled - No shoes in inventory.
6 - Capture a new shoe
7 - Exit {PROGRAM_NAME} program.
            ''')
        menu = input_valid(": ", ["6", "7"])

    # View all shoes
    if menu == "1":
        while True:
            print_header(PROGRAM_NAME, PROGRAM_SLOGAN, WIDTH)
            menu = view_shoes(menu_options=["1 - Return to main menu.\n"])
            if menu == "1":
                break

    # View a specific shoe.
    elif menu == "2":
        while True:
            print_header(PROGRAM_NAME, PROGRAM_SLOGAN, WIDTH)
            print()
            print("By which attribute would you like to search?\n",
                "1 - Country",
                "2 - Code",
                "3 - Product\n",
                "4 - Return to main menu\n",
                sep="\n")

            menu = input_valid(": ", ["1", "2", "3", "4",
                                    "country",
                                    "code",
                                    "product"])
            # Return to main menu
            if menu == "4":
                break

            search_list = []
            # Determine attribute selected by user
            if menu in ["country", "code", "product"]:
                clear_lines(9)
                attr_value = input(f"Please enter the {menu}\n: ")
                search_list = search_shoes_data(menu, attr_value)

            # If user input number
            elif 0 < int(menu) < 6:
                clear_lines(9)
                # menu is converted to an index for the list below:
                attribute = ["country", "code", "product"]
                # Determine attribute selected by user
                attr_value = input(f"Please enter the {attribute[int(menu) - 1]}\n: ")
                search_list = search_shoes_data(attribute[int(menu) - 1], attr_value)
                clear_lines(3)

            # If list contains values (If user searched a valid shoe):
            if search_list:
                view_shoes(search_list, enable_sorting=False)
            else:
                print("\nInvalid input.")
                input("Press ENTER to return to previous menu.")

    # View shoes on sale.
    elif menu == "3":
        print_header(PROGRAM_NAME, "Viewing shoes that needs to be sold ASAP!!!", WIDTH)
        view_shoes_sale()

    # View shoes that needs to be restocked.
    elif menu == "4":
        while True:
            print_header(PROGRAM_NAME, "The following shoes needs to be restocked:", WIDTH)
            menu = re_stock()
            if menu == "2":
                break

    # View summary.
    elif menu == "5":
        print_header(PROGRAM_NAME, "View Shoe summaries and nothing more!", WIDTH)
        print()
        view_shoe_summary()
        input("Press ENTER to return to main menu.")
        continue

    # Capture a new shoe.
    elif menu == "6":
        print_header(PROGRAM_NAME, "Capture a new shoe!", WIDTH)
        print()
        capture_shoes_data()
        continue

    # Exit program.
    elif menu == "7":
        print_header(PROGRAM_NAME, "Where you always come back!", WIDTH)
        print(f"Thank you for using {PROGRAM_NAME}. See you again soon!\n")
        break
