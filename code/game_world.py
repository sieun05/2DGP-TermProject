world = [[], [], []] # layers for game objects
collision_pairs = {} # dictionary

def add_object(o, depth):
    world[depth].append(o)

    for layer in world:
        layer.sort(key=lambda obj: obj.y, reverse=True)

def add_objects(ol, depth):
    world[depth] += ol

    for layer in world:
        layer.sort(key=lambda obj: obj.y, reverse=True)

def remove_object(o):
    for layer in world:
        if o in layer:
            remove_collision_object(o)
            layer.remove(o)
            return

    # 이미 삭제된 오브젝트를 다시 삭제하려고 할 때는 조용히 무시
    # (모드 전환 시 발생할 수 있는 정상적인 상황)
    pass

def update():
    for layer in world:
        layer.sort(key=lambda obj: obj.y, reverse=True)


        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()


def clear():
    global world, collision_pairs

    for layer in world:
        layer.clear()

    # 충돌 페어도 모두 정리하여 완전한 초기화
    collision_pairs.clear()

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def add_collision_pair(key, a, b):
    if key not in collision_pairs:
        collision_pairs[key] = [[], []]  # [list of a, list of b]
    if a:
        collision_pairs[key][0].append(a)
    if b:
        collision_pairs[key][1].append(b)

def handle_collisions():
    # 등록된 모든 충돌 그룹에 대해 충돌 검사 수행

    for key, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(key, b)
                    b.handle_collision(key, a)

def get_objects_by_type(object_type):
    """특정 타입의 오브젝트들을 반환"""
    objects = []
    for layer in world:
        for obj in layer:
            if isinstance(obj, object_type):
                objects.append(obj)
    return objects
