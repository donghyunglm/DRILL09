from pico2d import *

CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 1024
MOVE_SPEED = 5


def handle_events():
    global running
    global left_pressed, right_pressed, up_pressed, down_pressed

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                left_pressed = True
            elif event.key == SDLK_RIGHT:
                right_pressed = True
            elif event.key == SDLK_UP:
                up_pressed = True
            elif event.key == SDLK_DOWN:
                down_pressed = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                left_pressed = False
            elif event.key == SDLK_RIGHT:
                right_pressed = False
            elif event.key == SDLK_UP:
                up_pressed = False
            elif event.key == SDLK_DOWN:
                down_pressed = False


def update():
    global dir_x, dir_y, x, y

    # 눌림 상태로 계산하므로 반복 입력은 누적되지 않고 반대 입력은 상쇄된다.
    dir_x = int(right_pressed) - int(left_pressed)
    dir_y = int(up_pressed) - int(down_pressed)
    # 이벤트 유무와 관계없이 매 프레임 이동한다. 위쪽은 y가 증가한다.
    x += dir_x * MOVE_SPEED
    y += dir_y * MOVE_SPEED


def draw():
    clear_canvas()
    ground.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
    # 오른쪽 IDLE 첫 프레임. 행 좌표는 이미지 아래쪽을 기준으로 한다.
    character.clip_draw(0, 300, 100, 100, x, y)
    update_canvas()


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running = True
x = CANVAS_WIDTH // 2
y = CANVAS_HEIGHT // 2
dir_x = 0
dir_y = 0
left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False

while running:
    handle_events()
    update()
    draw()
    delay(0.01)

close_canvas()
