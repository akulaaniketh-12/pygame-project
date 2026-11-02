import pygame
pygame.init()
display_surface = pygame.display.set_mode((500,500))


text = pygame.font.Font(None,36).render("My first game screen",True,pygame.Color("Grey"))
text_rec = text.get_rect(center = (500 // 2,500 // 2 + 50))
def game_loop():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        s_w,s_h = 75,75
        s_c = pygame.Color('blue')
        display_surface.blit(text,text_rec)
        pygame.draw.rect(display_surface,s_c(s_w,s_h))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
game_loop()