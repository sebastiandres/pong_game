from games import ping_pong
from date import date_update
import sys

if __name__=="__main__":
    if len(sys.argv)==3:
        user = sys.argv[1]
        ball_path = sys.argv[2]
    else:
        user = "unknown_user"
        ball_path = "balls/simplest.txt"
    date_update.run(user)
    ping_pong.run(ball_path)