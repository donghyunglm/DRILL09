from pico2d import *
from pathlib import Path
from math import hypot

RESOURCE_DIR = Path(__file__).resolve().parent

CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 1024
MOVE_SPEED = 5
ANIMATION_SPEED = 0.2
FRAME_DELAY = 0.01
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
FRAME_COUNT = 8
CHARACTER_WIDTH = 100
CHARACTER_HEIGHT = 100

# 스프라이트 행 번호는 이미지 아래쪽부터 센다.
RUN_LEFT = 0
RUN_RIGHT = 1
IDLE_LEFT = 2
IDLE_RIGHT = 3


def reset_input():
    """모든 방향키의 눌림 상태를 초기화한다."""
    global left_pressed, right_pressed, up_pressed, down_pressed
    left_pressed = right_pressed = up_pressed = down_pressed = False


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
    global dir_x, dir_y, x, y, facing, action, frame

    # 눌림 상태로 계산하므로 반복 입력은 누적되지 않고 반대 입력은 상쇄된다.
    dir_x = int(right_pressed) - int(left_pressed)
    dir_y = int(up_pressed) - int(down_pressed)
    # 이벤트 유무와 관계없이 매 프레임 이동한다. 위쪽은 y가 증가한다.
    x += dir_x * MOVE_SPEED
    y += dir_y * MOVE_SPEED

    # 그리는 크기의 절반을 남겨 캐릭터 전체를 화면 안에 유지한다.
    half_width = CHARACTER_WIDTH / 2
    half_height = CHARACTER_HEIGHT / 2
    x = max(half_width, min(CANVAS_WIDTH - half_width, x))
    y = max(half_height, min(CANVAS_HEIGHT - half_height, y))

    # 좌우 이동만 바라보는 방향을 바꾼다. 상하 이동과 정지는 유지한다.
    if dir_x != 0:
        facing = dir_x

    if dir_x != 0 or dir_y != 0:
        next_action = RUN_RIGHT if facing == 1 else RUN_LEFT
    else:
        next_action = IDLE_RIGHT if facing == 1 else IDLE_LEFT

    # 동작이 바뀌면 첫 프레임부터, 유지되면 8프레임을 반복한다.
    if action != next_action:
        action = next_action
        frame = 0.0
    else:
        frame = (frame + ANIMATION_SPEED) % FRAME_COUNT


def draw():
    clear_canvas()
    ground.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
    character.clip_draw(
        int(frame) * FRAME_WIDTH, action * FRAME_HEIGHT,
        FRAME_WIDTH, FRAME_HEIGHT, x, y, CHARACTER_WIDTH, CHARACTER_HEIGHT
    )
    update_canvas()


def main():
    global ground, character, running, x, y, dir_x, dir_y
    global facing, action, frame
    global left_pressed, right_pressed, up_pressed, down_pressed

    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        ground = load_image(str(RESOURCE_DIR / 'TUK_GROUND.png'))
        character = load_image(str(RESOURCE_DIR / 'animation_sheet.png'))
        running = True
        x, y = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2
        dir_x = dir_y = 0
        facing = 1
        action = IDLE_RIGHT
        frame = 0.0
        reset_input()

        while running:
            handle_events()
            # 종료 입력을 받으면 다음 화면을 그리지 않고 루프를 끝낸다.
            if not running:
                break
            update()
            draw()
            delay(FRAME_DELAY)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
