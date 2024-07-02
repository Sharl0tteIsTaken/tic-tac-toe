from showmaker.showmaker import ShowMaker

dk_showmaker = ShowMaker()



operating = playing = True
while operating:
    dk_showmaker.new_game()
    playing = dk_showmaker.playing
    while playing:
        dk_showmaker.player_input()
        playing = dk_showmaker.playing
    operating = input("one more round?(Y/N): ") == 'Y'
print('Game Over.')
