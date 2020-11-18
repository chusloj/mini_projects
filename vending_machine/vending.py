import random
import os

def make_prices(num, price_range):

    """ Create a list of prices """
    prices = [random.randrange(
        price_range[0], price_range[1]) * 0.25 for _ in range(num)]
    return prices

def make_items(price_list):

    """ Create a list of items """

    items = []
    letters = ['A', 'B', 'C', 'D', 'E']
    for n in range(len(price_list)):
        l_count = n // 5
        items.append(f'{letters[l_count]}{(n%5)+1}')
    return items




def make_vending_machine(num, price_range):

    """ Create a vending machine """

    if num > 25:
        print("There cannot be more than 25 items in the vending machine.")
        raise ValueError

    prices = make_prices(num, price_range)
    items = make_items(prices)

    assert len(items) == len(prices)

    return items, prices




def make_descriptions(items):

    """ Create descriptions for the items in the vending machine """

    l = len(items)
    foods = ['chocolate', 'cookies', 'chips', 'soda']
    food_list = [random.choice(foods) for _ in range(l)]
    return food_list


def print_vending_machine(items, prices):  # keep text formatting here

    """ 
    Format the vending machine
    to fit nicely inside the command prompt
    and print it
    """

    for n in range(len(prices)):
        if (n + 1) % 5 == 0:
            item_line = [items[j] for j in range(n - 4, n + 1)]
            price_line = [f"${str(prices[k])}" for k in range(n - 4, n + 1)]

            for n, (p, i) in enumerate(zip(price_line, item_line)):
                if i != 'SOLD OUT':
                    len_diff = len(p) - len(i)
                    item_line[n] += (' ' * len_diff)
                else:
                    len_diff = int(8) - len(p)
                    price_line[n] += (' ' * len_diff)

            print(' || '.join(item_line))
            print(' || '.join(price_line))
            print('\n')




def runner():

    """ Defines the interface to the vending machine """

    print("How many entries would you like in your vending machine?",
    "Please keep the number of entries <= 25.")
    num = int(input())

    items, prices = make_vending_machine(num, [1, 8])
    food_list = make_descriptions(items)

    print("How much money do you have?")
    money = float(input())

    sold_out_list = []
    while (any(prices) != 'SOLD OUT') or (money > 0):
        if len(sold_out_list) == len(items):
            os.system('clear')
            print("This machine is empty!\n")
            print(f"You have ${money} remaining.\n")
            return

        print(f"You have ${money} remaining.\n")

        print_vending_machine(items, prices)

        print('\n')
        print("What's your selection?")

        choice = input()  # input is type: string by default

        os.system('clear')

        if choice in sold_out_list:
            print("This item is sold out! Please choose another item.")

        if str(choice) not in items:
            print("\n\nPlease choose a valid selection.\n\n")
            continue

        if money < prices[items.index(choice)]:
            print("You can't afford that! Make another selection.")
            continue

        money -= prices[items.index(choice)]
        sold_out_list.append(items[items.index(choice)])

        print(f"You got {food_list[items.index(choice)]}\n")

        # This lien has to be placed after all other lines
        items[items.index(choice)] = 'SOLD OUT'


# Driver
if __name__ == '__main__':
    runner()
