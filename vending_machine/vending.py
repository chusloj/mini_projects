import random

# make a 3-level vending machine with 15 items
def printed_vending_machine(num, price_range):

    if num>25:
        print("There cannot be more than 25 items in the vending machine.")
        raise ValueError

    def make_prices(num, price_range):
        prices = [f'${random.randrange(price_range[0], price_range[1]) * 0.25}' for _ in range(1, num+1)]
        return prices

    def make_items(price_list):
        items = []
        letters = ['A','B','C','D','E']
        for n, p in enumerate(price_list):
            l_count = n // 5
            ticker = f'{letters[l_count]}{(n%5)+1}'

            len_diff = len(p) - len(ticker)
            item = str(ticker + (' '*len_diff))
            items.append(item)
        return items




    prices = make_prices(num, price_range)
    items = make_items(prices)

    assert len(items) == len(prices)



    for n, (i,p) in enumerate(zip(items, prices)):
        if (n+1) % 5 == 0:
            item_line = [items[j] for j in range(n-4, n+1)]
            price_line = [prices[k] for k in range(n-4,n+1)]
            print(' || '.join(item_line))
            print(' || '.join(price_line))
            print('\n')



# Driver
def main():
    print("How much money do you have?")
    money = input()
    print(f"You have ${money} remaining.")

    print("\nMake a selection\n")

    printed_vending_machine(15, [1,8])

    print('\n')
    print("What's your selection?")

    selection = input()

    # TODO: separate prices/items functions so you can
    # return the prices/inputs list, replace the choice
    # with 'SOLD OUT', and then print the list again

    # TODO: throw error when a choice that is "SOLD OUT"
    # is made

    # TODO: make message that says "Machine is empty!"
    # When the machine is empty


# Driver
main()

