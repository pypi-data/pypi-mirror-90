def main():
    print('Welcome to AIO Toolbox')
    while True:
        print('------------------------------------------')
        print('Mode 1: Currency Conversion Calculater')
        print('Mode 2: eBay View bot')
        print('Mode 3: Random Password generator')
        print('Mode 4: US Mint ATC Link Generator ')
        print('Mode 5: SNKR Early link Gen')
        mode_choice = input('What mode would you like to use? ')

        if mode_choice == '1':
            import Currency_conversion
            Currency_conversion.currency_convert()
            choice_x = input('Type F to close the program and A to use another module ')
            if choice_x == 'F':
                quit()
            elif choice_x == 'A':
                pass
        elif mode_choice == '2':
            import ebayviewer
            ebayviewer.start()
            choice_x = input('Type F to close the program and A to use another module ')
            if choice_x == 'F':
                quit()
            elif choice_x == 'A':
                pass
        elif mode_choice == '3':
            import randompassgen
            randompassgen.start()
            choice_x = input('Type F to close the program and A to use another module ')
            if choice_x == 'F':
                quit()
            elif choice_x == 'A':
                pass
        elif mode_choice == '4':
            import usmint_atc
            usmint_atc.start()
            choice_x = input('Type F to close the program and A to use another module ')
            if choice_x == 'F':
                quit()
            elif choice_x == 'A':
                pass
        elif mode_choice == '5':
            import snkrs_el
            snkrs_el.start()
            choice_x = input('Type F to close the program and A to use another module ')
            if choice_x == 'F':
                quit()
            elif choice_x == 'A':
                pass

if __name__ == "__main__":
    main()