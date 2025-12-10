from pico2d import *

import game_framework
import game_world
from item_select import SelectItem
import common

image = None
image2 = None
font = None
select_item1, select_item2, select_item3 = None, None, None

def init():
    global image, image2, select_item1, select_item2, select_item3, font
    image = load_image('images/item.png')
    image2 = load_image('images/lobby.png')
    font = load_font('images/ENCR10B.TTF', 16)

    select_item1 = SelectItem(265, 330, 'power')
    select_item2 = SelectItem(400, 330, 'speed')
    select_item3 = SelectItem(535, 330, 'maxhp')

def finish():
    global image, image2, select_item1, select_item2, select_item3, font
    del image
    del image2
    del select_item1
    del select_item2
    del select_item3
    del font

def update():
    game_world.update()
    pass

def draw():
    clear_canvas()
    image2.draw(400,300)
    game_world.render()
    image.draw(400, 300)

    select_item1.draw()
    select_item2.draw()
    select_item3.draw()

    font.draw(655, 530, f'{common.gear}', (0, 0, 0))
    font.draw(655, 530, f'{common.gear}', (0, 0, 0))

    update_canvas()

#이벤트 변경해야함
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        # ESC / SPACE는 기존 동작 유지
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.pop_mode()
        # 마우스 왼쪽 클릭 처리: 선택 아이템의 바운딩박스와 비교
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            try:
                mx = event.x
                my = 600 - event.y
            except Exception:
                mx = None
                my = None

            if mx is not None and my is not None:
                for it in (select_item1, select_item2, select_item3):
                    if it is None:
                        continue
                    try:
                        left, bottom, right, top = it.get_bb()
                    except Exception:
                        continue
                    if left <= mx <= right and bottom <= my <= top:
                        # 클릭된 아이템 적용
                        try:
                            applied = it.clicked()
                            if applied:
                                print(f"Item '{it.kind}' applied")
                        except Exception:
                            pass
                        break

def pause():
    pass


def resume():
    pass