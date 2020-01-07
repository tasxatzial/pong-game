"""Pong game"""

import simplegui
import random

WIDTH, HEIGHT = 800, 600
PAD_WIDTH = WIDTH // 100
PAD_HEIGHT = HEIGHT // 6
HALF_PAD_HEIGHT = PAD_HEIGHT / 2.0
MIN_PAD_WIDTH = WIDTH // 140
MAX_PAD_WIDTH = WIDTH // 60
MIN_PAD_HEIGHT = HEIGHT // 16
MAX_PAD_HEIGHT = HEIGHT // 4
PAD_SPEED = HEIGHT // 100
MIN_PAD_SPEED = HEIGHT // 140
MAX_PAD_SPEED = HEIGHT // 50
paddle_lpos = paddle_rpos = HEIGHT / 2.0
paddle_lvel = paddle_rvel = 0
BALL_RADIUS = min(HEIGHT, WIDTH - 2 * PAD_WIDTH) // 28
MIN_BALL_RADIUS = min(HEIGHT, WIDTH - 2 * PAD_WIDTH) // 64
MAX_BALL_RADIUS = min(HEIGHT, WIDTH - 2 * PAD_WIDTH) // 16
ball_pos = [0, 0]
ball_vel = [0, 0]

paused = 1
score_left = score_right = 0
SPEED_LIM = 2000

def spawn_ball(direction):
    """Initializes ball's position and velocity

    direction is either 'LEFT' or 'RIGHT'    
    """
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2.0, HEIGHT / 2.0]
    x = random.randrange(WIDTH // 6, WIDTH // 3) / 60.0
    y = random.randrange(HEIGHT // 6, HEIGHT // 3) / 60.0
    updown = random.choice(['UP', 'DOWN'])
    if updown == 'UP' and direction == 'RIGHT':
        ball_vel = [x, -y]
    elif updown == 'UP' and direction == 'LEFT':
        ball_vel = [-x, -y]
    elif updown == 'DOWN' and direction == 'RIGHT':
        ball_vel = [x, y]
    else:
        ball_vel = [-x, y]


def new_game():
    """Starts a new game"""
    global paddle_lpos, paddle_rpos, score_left, score_right
    global paused
    score_left = score_right = 0
    paddle_lpos = paddle_rpos = HEIGHT / 2.0
    spawn_ball(random.choice(['LEFT', 'RIGHT']))
    button_start_pause.set_text('Go!')
    paused = 1


def start_pause():
    """Starts/pauses game"""
    global paused
    paused = not paused
    if paused:
        button_start_pause.set_text('Go!')
    else:
        button_start_pause.set_text('Pause')


def draw(canvas):
    """Handles the drawing on the canvas"""
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2.0, 0], [WIDTH / 2.0, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],
                     [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'Green', 'Green')
    
    # draw paddles
    y1 = paddle_lpos - HALF_PAD_HEIGHT
    y2 = paddle_lpos + HALF_PAD_HEIGHT
    canvas.draw_polygon([(0, y1), (0, y2),
                        (PAD_WIDTH, y2), (PAD_WIDTH, y1)], 1, 'Red','Red')
    y1 = paddle_rpos - HALF_PAD_HEIGHT
    y2 = paddle_rpos + HALF_PAD_HEIGHT
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, y1), (WIDTH - PAD_WIDTH, y2),
                        (WIDTH, y2), (WIDTH, y1)], 1, 'Red','Red')
    
    # draw scores
    size = min(HEIGHT, WIDTH - 2 * PAD_WIDTH) // 16
    s1 = frame.get_canvas_textwidth(str(score_left), size)
    canvas.draw_text(str(score_left), (WIDTH//2 - s1 - 40, HEIGHT // 6), size, 'White')
    canvas.draw_text(str(score_right), (WIDTH//2 + 30, HEIGHT // 6), size, 'White')
    
    # advance the game
    if not paused:
        run_game()


def run_game():
    """Updates ball's position/velocity, controls paddle movement,
    updates scores
    """
    global score_left, score_right, paddle_rpos, paddle_lpos
    
    # spawn new ball in random direction if ball's speed exceeds limit
    if ball_vel[0] > SPEED_LIM:
        spawn_ball(random.choice(['LEFT', 'RIGHT']))
        
    # check if ball hit the right gutter
    if ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        
        # if ball hit the right paddle: update ball velocity/position
        if (paddle_rpos - HALF_PAD_HEIGHT <= ball_pos[1] and
                paddle_rpos + HALF_PAD_HEIGHT >= ball_pos[1]):
            ball_updatex(WIDTH - BALL_RADIUS - PAD_WIDTH - 0.01)
            
        # else update score, spawn new ball
        else:
            score_left += 1
            spawn_ball('LEFT')
            
    # elif ball hit the left gutter
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        
        # if ball hit the left paddle: update ball velocity/position
        if (paddle_lpos - HALF_PAD_HEIGHT <= ball_pos[1] and
                paddle_lpos + HALF_PAD_HEIGHT >= ball_pos[1]):
            ball_updatex(PAD_WIDTH + BALL_RADIUS + 0.01)
        
        # else update score, spawn new ball
        else:
            score_right += 1
            spawn_ball('RIGHT')

    # elif ball hit the bottom of the canvas: update ball velocity/position
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_updatey(HEIGHT - BALL_RADIUS - 0.01)
 
    # elif ball hit the top of the canvas: update ball velocity/position
    elif ball_pos[1] <= BALL_RADIUS:
        ball_updatey(BALL_RADIUS + 0.01)

    # else update only ball's position
    else:
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    
    # update paddle position, keep paddles on the canvas
    x = paddle_rpos + paddle_rvel
    if (HALF_PAD_HEIGHT <= x <= HEIGHT - HALF_PAD_HEIGHT):
        paddle_rpos = x
    x = paddle_lpos + paddle_lvel
    if (HALF_PAD_HEIGHT <= x <= HEIGHT - HALF_PAD_HEIGHT):
        paddle_lpos = x


def ball_updatex(pos):
    """Updates position/velocity of the ball when it hits left/right paddle.
    Ball is also re-positioned (in case it goes past the paddle).
    
    pos: horizontal coordinate of the center of the ball when it hits the gutter
    """
    f1 = (ball_pos[0] - pos) * ball_vel[1] / ball_vel[0]
    ball_pos[0] = pos
    ball_pos[1] -= f1
    ball_vel[0] *= -1.1
    
def ball_updatey(pos):
    """Updates position/velocity of the ball when it hits bottom/top edge.
    Ball is also re-positioned (in case it goes past the edge).
    
    pos: vertical coordinate of the center of the ball when it hits the edge
    """
    f1 = (pos - ball_pos[1]) * ball_vel[1] / ball_vel[0]
    ball_pos[0] -= f1
    ball_pos[1] = pos
    ball_vel[1] *= -1.03


def keydown(key):
    """Changes paddle velocity on key-down"""
    global paddle_lvel, paddle_rvel
    if key == simplegui.KEY_MAP['up']:
        paddle_rvel -= PAD_SPEED
    elif key == simplegui.KEY_MAP['down']:
        paddle_rvel += PAD_SPEED
    elif key == simplegui.KEY_MAP['w']:
        paddle_lvel -= PAD_SPEED
    elif key == simplegui.KEY_MAP['s']:
        paddle_lvel += PAD_SPEED


def keyup(key):
    """Changes paddle velocity on key-up"""
    global paddle_lvel, paddle_rvel
    if key == simplegui.KEY_MAP['up']:
        paddle_rvel += PAD_SPEED
    elif key == simplegui.KEY_MAP['down']:
        paddle_rvel -= PAD_SPEED
    elif key == simplegui.KEY_MAP['W']:
        paddle_lvel += PAD_SPEED
    elif key == simplegui.KEY_MAP['s']:
        paddle_lvel -= PAD_SPEED


def ball_size(size):
    """Sets ball radius to the specified size"""
    global BALL_RADIUS
    if MIN_BALL_RADIUS <= int(size) <= MAX_BALL_RADIUS:
        BALL_RADIUS = int(size)

def paddle_size(size):
    """Sets paddle height to the specified size"""
    global PAD_HEIGHT, HALF_PAD_HEIGHT
    if MIN_PAD_HEIGHT <= int(size) <= MAX_PAD_HEIGHT:
        PAD_HEIGHT = int(size)
        HALF_PAD_HEIGHT = PAD_HEIGHT / 2.0

def paddle_speed(size):
    """Sets paddle speed to the specified size"""
    global PAD_SPEED
    if MIN_PAD_SPEED <= int(size) <= MAX_PAD_SPEED:
        PAD_SPEED = int(size)

def paddle_width(size):
    """Sets paddle width to the specified size"""
    global PAD_WIDTH
    if MIN_PAD_WIDTH <= int(size) <= MAX_PAD_WIDTH:
        PAD_WIDTH = int(size)

# create frame and register control handlers
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
button_start_pause = frame.add_button('Go!', start_pause, 100)
frame.add_button('Restart', new_game, 100)
inp_ball_radius = frame.add_input(
                    'Enter ball radius (' + str(MIN_BALL_RADIUS) + '-' +
                     str(MAX_BALL_RADIUS) + ')', ball_size, 50)
inp_ball_radius.set_text(str(BALL_RADIUS))
inp_pad_height = frame.add_input(
                    'Enter paddle size (' + str(MIN_PAD_HEIGHT) + '-' +
                    str(MAX_PAD_HEIGHT) + ')', paddle_size, 50)
inp_pad_height.set_text(str(PAD_HEIGHT))
inp_pad_speed = frame.add_input(
                    'Enter paddle speed (' + str(MIN_PAD_SPEED) + '-' +
                    str(MAX_PAD_SPEED) + ')', paddle_speed, 50)
inp_pad_speed.set_text(str(PAD_SPEED))
inp_pad_width = frame.add_input(
                    'Enter paddle width (' + str(MIN_PAD_WIDTH) + '-' +
                    str(MAX_PAD_WIDTH) + ')', paddle_width, 50)
inp_pad_width.set_text(str(PAD_WIDTH))
frame.add_label('Controls:')
frame.add_label('Left player: W,S')
frame.add_label('Right player: Up, Down')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame and spawn ball
frame.start()
spawn_ball(random.choice(['LEFT', 'RIGHT']))