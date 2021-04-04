from os.path import dirname, realpath
from os.path import join as join_path
from PIL import Image, ImageDraw, ImageFont


def draw_centered(draw, x, y, msg, font, fill):
    """
    Draws a centered text
    """
    w, h = draw.textsize(msg, font=font)
    draw.text((int(x-w/2), int(y-h/2)), msg, font=font, fill=fill)
    return


def create_gif(date, ball, gif_path, font_path):
    """
    Creates a gif with the provided parameters
    """
    # Play the game
    HEIGHT = 200
    WIDTH = 800
    BBOX = 25
    N_PLAYS = 2
    DURATION = 1 * 100

    # Some calculations
    H_aux = (HEIGHT - 2*BBOX)/3
    date_x, date_y = int(WIDTH/2), int(BBOX + H_aux)
    ping_x, ping_y = BBOX, int(BBOX + 2*H_aux)
    pong_x, pong_y = WIDTH-BBOX, int(BBOX + 2*H_aux)
    n_positions = int((WIDTH-2*BBOX)/5)

    # Create the individual frames as png images
    im = Image.new("RGB", (WIDTH, HEIGHT), 'white')
    images = []
    small_font = ImageFont.truetype(font_path, 20)
    big_font = ImageFont.truetype(font_path, 30)

    for play in range(N_PLAYS):
        for position in range(1, n_positions-1):
            position = ping_x + int(position*(WIDTH - 2*BBOX)/n_positions)
            if play % 2 == 0:
                left_spaces = position
            else:
                left_spaces = WIDTH - position
            frame = im.copy()
            d = ImageDraw.Draw(frame)
            draw_centered(d, date_x, date_y, date, small_font, "grey")
            draw_centered(d, ping_x, ping_y, "|", big_font, "red")
            draw_centered(d, left_spaces, ping_y, ball, big_font, "black")
            draw_centered(d, pong_x, pong_y, "|", big_font, "red")
            images.append(frame)

    # Save the frames as an animated GIF with given name
    print(gif_path)
    images[0].save(gif_path,
                   save_all=True,
                   append_images=images[1:],
                   duration=DURATION,
                   loop=0)

    # Save the frames as an animated GIF as latest.gif
    latest_gif_path = "/".join(gif_path.split("/")[:-1]) + "/latest.gif"
    print(latest_gif_path)
    images[0].save(latest_gif_path,
                   save_all=True,
                   append_images=images[1:],
                   duration=DURATION,
                   loop=0)


def run(ball_path):
    """
    Get the ball rolling
    """
    # Get a reliable path for reading the files
    file_path = dirname(realpath(__file__))
    main_path = join_path(file_path, "..")

    # See if a given file has been given
    ball_path = join_path(main_path, ball_path)
    print(ball_path)

    # Get the ball
    with open(ball_path) as f:
        ball = f.read()[0]  # Just get the first char. Nothing else.

    # Get the date
    date_path = join_path(main_path, "date/ever_changing_date_file.txt")
    with open(date_path) as f:
        date = f.read().strip()

    # Create the gif path
    gif_path = ball_path.replace("/balls/", "/gifs/").replace(".txt", ".gif")

    # Font path
    font_path = join_path(main_path, "fonts/Symbola.ttf")

    # Create the gif
    create_gif(date, ball, gif_path, font_path)

    return
