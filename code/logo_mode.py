from pico2d import *
import game_framework

image = None
logo_start_time = 0

def init():
    global image, logo_start_time
    image = load_image('images/tuk_credit.png')
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    if get_time() - logo_start_time > 50:
        #game_framework.change_mode(title_mode)
        game_framework.quit()

def draw():
    clear_canvas()
    # 이미지 로드 실패(또는 아직 로드되지 않음)를 안전하게 처리
    if image:
        image.draw(400, 300)
    update_canvas()
    pass

def handle_events():
    #로고 시간에 들어온 이벤트들을 버퍼로부터 가져오고 삭제한다.
    event_list = get_events()
    # no nothing to handle

def pause():
    pass

def resume():
    pass