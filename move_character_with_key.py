from pico2d import *


open_canvas()
grass = load_image('grass.png')
character = load_image('animation_sheet.png')


def handle_events():
    global running
    global left_pressed, right_pressed
    # fill here

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                right_pressed = True
            elif event.key == SDLK_LEFT:
                left_pressed = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                right_pressed = False
            elif event.key == SDLK_LEFT:
                left_pressed = False
        # fill here


running = True
x = 800 // 2
frame = 0
left_pressed = False
right_pressed = False
previous_time = get_time()
animation_time = 0.0

while running:
    handle_events()
    current_time = get_time()
    elapsed = current_time - previous_time
    previous_time = current_time
    x += (int(right_pressed) - int(left_pressed)) * 200 * elapsed
    animation_time += elapsed
    frame = int(animation_time / 0.05) % 8
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 100, 100, 100, x, 90)
    update_canvas()

    delay(0.01)

# fill here


close_canvas()

