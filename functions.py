import pygame

from itertools import chain


# used for text wrapping
def truncline(text, font, maxwidth):
    real = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    old = None
    while l > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        l = font.size(stext)[0]
        real = len(stext)
        done = 0
    return real, done, stext


# used for text wrapping
def wrapline(text, font, maxwidth):
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


# used for text wrapping
def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)


# checks if 2 rectangles are in a certain range of each other
def inrange(rect1, rect2, range):
    range1 = pygame.Rect(rect1.x - range / 2, rect1.y - range / 2, range, range)
    range2 = pygame.Rect(rect1.right - range / 2, rect1.bottom - range / 2, range, range)

    if range1.colliderect(rect2) or range2.colliderect(rect2):
        return True
    return False


# checks if 2 rectangles are in a certain range of each other on the x axis
def inrange_x(rect1, rect2, range):
    range1 = pygame.Rect(rect1.x - range / 2, rect2.y, range, range)
    range2 = pygame.Rect(rect1.right - range / 2, rect2.y, range, range)

    if range1.colliderect(rect2) or range2.colliderect(rect2):
        return True
    return False


# checks if 2 rectangles are in a certain range of each other on the y axis
def inrange_y(rect1, rect2, range):
    range1 = pygame.Rect(rect2.x, rect1.y - range / 2, range, range)
    range2 = pygame.Rect(rect2.x, rect1.bottom - range / 2, range, range)

    if range1.colliderect(rect2) or range2.colliderect(rect2):
        return True
    return False


# finds the closest rect to the base rectangle out of a list of rectangles
def findclosest(base, objects):
    winner = 9999
    winobj = None

    for obj in objects:

        distances = [base.rect.x - obj.rect.x,
                     base.rect.y - obj.rect.y,
                     base.rect.right - obj.rect.x,
                     base.rect.bottom - obj.rect.y,
                     base.rect.x - obj.rect.right,
                     base.rect.y - obj.rect.bottom,
                     base.rect.right - obj.rect.right,
                     base.rect.bottom - obj.rect.bottom]

        for i in range(len(distances)):

            if distances[i] < 0:
                distances[i] -= distances[i] * 2

        distance = sum(distances)

        if distance < winner:
            winner = distance
            winobj = obj

    return winobj
