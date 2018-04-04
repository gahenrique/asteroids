import pygame as pg


def writeScore(text, score):
    f = open("Score.txt", 'r+')
    x = text + ":" + str(score) + "\n"
    lines = f.readlines()
    for i in range(0,len(lines) - 1):
        split = lines[i].split(":")
        number = int(split[1])
        print(number)
        if score > number:
            lines.insert(i,x)
            break
    g = open("Score.txt", 'r+')
    for i in range(0, len(lines)):
        g.write(lines[i])
    g.close()
    f.close()


def main(screen, resolution, FPS, clock, score):
    font = pg.font.Font(None, 32)
    input_box = pg.Rect(100, 100, 140, 32)
    done_button = font.render("OK", True, (255, 255, 255), (0, 200, 0))
    done_buttonRect = pg.Rect(100, 200, done_button.get_width(), done_button.get_height())

    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = True

    while done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = False
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                if done_buttonRect.collidepoint(event.pos):
                    writeScore(text, score)
                    done = False
                else:
                    active = True
                # Change the current color of the input box.
                color = color_active if active else color_inactive

            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    elif len(text) < 6:
                        text += event.unicode
        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(100, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)
        screen.blit(done_button, done_buttonRect)
        pg.display.flip()
        clock.tick(FPS)
