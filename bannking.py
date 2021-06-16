import random
import sqlite3
import sys

conn = sqlite3.connect('card.s3db')


def create_table():
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")


def add_card(id_, number, pin):
    cur = conn.cursor()
    cur.execute(F"INSERT INTO card (id, number, pin) VALUES ({id_}, {number}, {pin});")


def get_card(number):
    cur = conn.cursor()
    return cur.execute(F"SELECT * FROM card WHERE number = {number};").fetchall()


def get_all_card():
    cur = conn.cursor()
    return cur.execute("SELECT number FROM card;").fetchall()


def update_balance(new_balance, number):
    cur = conn.cursor()
    return cur.execute(F" UPDATE card SET balance = {new_balance} WHERE number = {number};")


def delete_account(number):
    cur = conn.cursor()
    return cur.execute(F"DELETE FROM card WHERE number = {number}")


def luhn_algorithm(card_number):
    number = []
    for i in range(len(card_number)):
        if (i + 1) % 2 == 1:
            if int(card_number[i]) * 2 > 9:
                number.append(int(card_number[i]) * 2 - 9)
            else:
                number.append(int(card_number[i]) * 2)
        else:
            number.append(int(card_number[i]))
    if sum(number) % 10 != 0:
        return card_number + str(10 - (sum(number) % 10))
    else:
        return card_number + '0'


def create_account():
    card_number = '400000' + str(random.randint(100000000, 999999999))
    card_pin = str(random.randint(1000, 9999))
    card_number = luhn_algorithm(card_number)
    print('Your card has been created')
    add_card(len(get_all_card()), card_number, card_pin)
    conn.commit()
    print('Your card number:', card_number, sep='\n')
    print('Your card PIN:', card_pin, sep='\n')


def log_account():
    card_number = input('Enter your card number:')
    card_pin = input('Enter your PIN:')

    if len(get_card(card_number)) != 0:
        if card_number in get_card(card_number)[0][1] and get_card(card_number)[0][2] == card_pin:
            print('You have successfully logged in!')
            option = None
            while option != 0:
                print('1. Balance')
                print('2. Add income')
                print('3. Do transfer')
                print('4. Close account')
                print('5. Log out')
                print('0. Exit')
                option = input()
                if option == '1':
                    print(get_card(card_number)[0][3])
                elif option == '2':
                    income = int(input())
                    old_balance = get_card(card_number)[0][3]
                    update_balance(old_balance + income, card_number)
                    conn.commit()
                    print('Income was added!')
                elif option == '3':
                    print('Transfer')
                    new_card = input()
                    if new_card == luhn_algorithm(new_card[:-1]):
                        if new_card != card_number:
                            status_card = 0
                            for i in get_all_card():
                                if new_card in i:
                                    status_card += 1
                            if status_card != 0:
                                print('Enter how much money you want to transfer:')
                                transfer = int(input())
                                if get_card(card_number)[0][3] >= transfer:
                                    old_balance = get_card(card_number)[0][3]
                                    now_balance = get_card(new_card)[0][3]
                                    update_balance(now_balance + transfer, new_card)
                                    update_balance(old_balance - transfer, card_number)
                                    conn.commit()
                                    print('Success!')
                                else:
                                    print('Not enough money!')
                            else:
                                print('Such a card does not exist.')
                        else:
                            print('You can\'t transfer money to the same account!')
                    else:
                        print('Probably you made a mistake in the card number.\nPlease try again!')

                elif option == '4':
                    delete_account(card_number)
                    conn.commit()
                    print('The account has been closed!\n')
                    break
                elif option == '5':
                    print('You have successfully logged out!')
                    break
                elif option == '0':
                    print('Bye!')
                    sys.exit()
        else:
            print('Wrong card number or PIN!')
    else:
        print('Wrong card number or PIN!')


choice = None
create_table()

while choice != 0:
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    choice = input('Your choice: ')
    if choice == '1':
        create_account()
    elif choice == '2':
        log_account()
    elif choice == '0':
        print('Bye!')
        break
