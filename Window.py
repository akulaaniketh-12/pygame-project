import pygame
pygame.init()
display_surface = pygame.display.set_mode((500,500))
pygame.display.set_caption("Car")
bgi = pygame.transform.scale(pygame.image.load("car.png").convert(),(500,500))
bi = pygame.transform.scale(pygame.image.load("dog.jpeg").convert_alpha(),(50,50))
text = pygame.font.Font(None,36).render("Hi I like cars and dogs",True,pygame.Color("Grey"))
text_rec = text.get_rect(center = (500 // 2,500 // 2 + 50))
def game_loop():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display_surface.blit(bgi,(0,0))
        display_surface.blit(bi,(50,50))
        display_surface.blit(text,text_rec)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
game_loop()
