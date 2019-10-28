import Character

# Returns line in form of (m, b) y = mx +b
# Y = MX + B
# M = (by-ay/bx-ax)
# B = ay - (by-ay/bx-ax)ax
# TODO: x != x


def is_collision(character_a, character_b):
    return character_a.rectangle.colliderect(character_b.rectangle)
