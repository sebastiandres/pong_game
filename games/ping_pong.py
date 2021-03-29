import time
import sys
from os.path import dirname, realpath
from os.path import join as join_path

def run():
    # Get a reliable path for reading the files
    file_path = dirname(realpath(__file__)) 
    main_path = join_path(file_path, "..") 

    # See if a given file has been given
    if len(sys.argv)==2:
        ball_path = sys.argv[1]
    else:
        ball_path = join_path(main_path, "balls/simplest.txt")

    # Get the ball
    with open(ball_path) as f:
        ball = f.read()[0] # Just get the first char. Nothing else.

    # Get the date
    date_path = join_path(main_path, "date/ever_changing_date_file.txt")
    with open(date_path) as f:
        date = f.read().strip()
    
    # Play the game
    print("Date: ", date)
    TABLE_LENGTH = 50
    N_PLAYS = 5
    PLAY_TIME = 1.0
    for play in range(N_PLAYS):
        for position in range(TABLE_LENGTH):
            if play % 2 == 0:
                left_spaces = " " * position
                right_spaces = " " * (TABLE_LENGTH - position)
            else:
                left_spaces = " " * (TABLE_LENGTH - position)
                right_spaces = " " * position
            print(f'|{left_spaces}{ball}{right_spaces}|', end='\r')
            time.sleep(PLAY_TIME/TABLE_LENGTH)
    print("\n") # Get a new clean line
