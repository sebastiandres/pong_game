from datetime import datetime
import sys

def get_message_string(user):
    """
    Creates a message with a user and the current time
    """
    now = datetime.now()
    day_string = now.strftime("%d/%m/%Y")
    hour_string = now.strftime("%H:%M:%S")
    message = now.strftime(f"Actualizado por {user} a las %{hour_string} del {day_string}\n")
    print(message)
    return message

def write_datefile(message, datetime_file="./date/ever_changing_date_file.txt"):
    """
    Writes the message to a files
    """    
    # Update the file
    with open(datetime_file, "w") as date_file:
        date_file.write(message+"\n")

def run(user):
    """
    Updates the date message with the given user
    """
    msg = get_message_string(user)
    write_datefile(msg)
    return

if __name__=="__main__":
    if len(sys.argv)==2:
        user = sys.argv[1]
    else:
        user = "unknown_user"
    msg = get_message_string(user)
    write_datefile(msg)