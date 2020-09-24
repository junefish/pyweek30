import pygame

pygame.init()

screen_width = 800
screen_height = 600
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255, 95)
disy = 300
font = pygame.font.Font(None, 32)
screen = pygame.display.set_mode([screen_width, screen_height])
selected = 0
rectsize = (192, 32)
end = 0
menu1 = ["New Game", "High Scores", "About", "Help", "Quit"]
menu2 = ["Key Bindings", "Resolution"]
menu3 = ["Written by:", "Bung", "Tucan444", "halfsickofshadows",
         "Turyam", "and whywhyy", "for pyweek30"]
menu4 = ["Arrow keys move", "Q is quit", "Esc is menu", "Space is pause"]
menulen = 0
menu = menu1


def menulogic():
    global menu
    global end
    global selected
    if menu == menu1:
        if selected == 0:
            print("new game def")
        if selected == 1:
            print("high scores def")
        if selected == 2:
            menu = menu3
            dispmenu()
        if selected == 3:
            menu = menu4
            dispmenu()
        if selected == 4:
            end = 1
        return


def dispmenu():
    global disy
    global menulen
    screen.fill(BLACK)
    background = pygame.image.load("assets/textures/menu.png").convert()
    image1 = pygame.Surface((800,  600))
    image1 = image1.convert()
    image1.blit(background, (0, 0))
    screen.blit(image1, (0, 0))
    pygame.display.flip()
    for a in range(len(menu)):
        menulen = a
        score1 = str(menu[a]).encode("utf-8").decode("utf-8")
        disscore = font.render(score1,  True,  RED)
        screen.blit(disscore,  [350, disy])
        scorerect = pygame.Rect((350,  disy), (rectsize))
        if selected == a and menu == menu1:
            highlight()
        pygame.display.update(scorerect)
        disy = disy + 32
    disy = 300


def highlight():
    highlight = pygame.Surface((rectsize), pygame.SRCALPHA)
    pygame.draw.rect(highlight, BLUE, highlight.get_rect(), 0)
    screen.blit(highlight,  (350, disy))


def up():
    global selected
    if selected == 0:
        selected = menulen
    else:
        selected = selected - 1


def down():
    global selected
    if selected == menulen:
        selected = 0
    else:
        selected = selected + 1


dispmenu()
while end == 0:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up()
                dispmenu()
            if event.key == pygame.K_DOWN:
                down()
                dispmenu()
            if event.key == pygame.K_ESCAPE:
                end = 1
            if event.key == pygame.K_RETURN:
                menulogic()
        if event.type == pygame.MOUSEMOTION:
            position = event.pos
            x = position[0]
            y = position[1]
            z = disy
            if x < 350 or x > 542:
                break
            if y < 300:
                break
            for i in range(len(menu)):
                if y >= (300 + (32 * i)) and y <= (300 + (32 * (i + 1))):
                    selected = i
                    dispmenu()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            menulogic()
