import csv


def ReadFile(file):
    """Reads a .csv and returns it as a 2 dimensional list."""
    arr = []
    with open(file, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            arr.append(row)
    f.close()
    return arr


members = ReadFile('members.csv')


def addMember(file, ):
    user = input('What is the new members name?')
    while True:
        elo = input(f"What is {user}'s elo? ")
        try:
            elo = float(elo)
            break
        except ValueError:
            print('Please enter a valid number')

    members.append([user, elo])
    print(members)
    with open(file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(members)
        f.close()


def updateElo(members, result, player_1, player_2, names):
    # Get elo from members.csv, get result from games_database.csv, calculate elo, update elo.
    whitePos = names.index(player_1)
    blackPos = names.index(player_2)

    whiteElo = float(members[whitePos][1])
    blackElo = float(members[blackPos][1])
    winner = 'Who won?'
    if result == '(1-0)':
        winner = 'White'
    elif result == '(0-1)':
        winner = 'Black'
    else:
        WhiteScore = 1 / 2
        BlackScore = 1 / 2

    D = 400
    K = 32

    if winner == 'White':
        WhiteScore = 1
        BlackScore = 0
    elif winner == 'Black':
        WhiteScore = 0
        BlackScore = 1

    Xscore = 1 / (1 + 10 ** ((whiteElo - blackElo) / D))
    UpdWhite = whiteElo + K * (WhiteScore - Xscore)

    Xscore = 1 / (1 + 10 ** ((blackElo - whiteElo) / D))
    UpdBlack = whiteElo + K * (BlackScore - Xscore)

    return [round(UpdWhite, 2), round(UpdBlack, 2)]


def addGame(members, games):
    names = []
    for row in members:
        names.append(row[0])
    print(names)
    m1 = input('Who was white in this game?\n')
    while True:
        if m1 not in names:
            check = ('Please enter a valid member or type add_member if they are new.')
            if check == 'add_member':
                addMember(members)
            else:
                m1 = check
        else:
            break

    while True:
        m2 = input('Who was black in this game?\n')
        if m2 not in names:
            check = input('Please enter a valid member or type add_member if they are new.')
            if check == 'add_member':
                addMember(members)
            else:
                m2 = check
        else:
            break

    while True:
        result = input('What was the result of the game, (1-0) / (0-1) / (1/2 - 1/2)\n')
        if result == '(1-0)' or result == '(0-1)' or result == '(1/2 - 1/2)':
            break
        else:
            print('Please enter (1-0), (0-1) or (1/2 - 1/2)')

    whitePos = names.index(m1)
    blackPos = names.index(m2)

    whiteElo = float(members[whitePos][1])
    blackElo = float(members[blackPos][1])

    with open(games, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        data = [f'{m1} ({whiteElo})', f'{m2} ({blackElo})', result]
        writer.writerow(data)
        f.close()

    updated = updateElo(members, result, m1, m2, names)
    print(updated)
    members[whitePos][1] = updated[0]
    members[blackPos][1] = updated[1]

    return members


def main():
    print('1: Add new member \n2: Add game to database & update elo')

    while True:
        option = input('Which option would you like to add')
        if option == '1':
            addMember('members.csv')
            break
        elif option == '2':
            addGame(members, 'games_database.csv')
            break
        else:
            print('Please say 1 or 2')

    with open('members.csv', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(members)
        f.close()


if __name__ == '__main__':
    main()
