import pygame
import sys
import random


pygame.init()


screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("게임 메뉴")

character_image = pygame.image.load('character.png')
obstacle_image = pygame.image.load('obstacle.png')
background_image = pygame.image.load('background.png')
target_image = pygame.image.load('target.png')

character_image = pygame.transform.scale(character_image, (130, 80))
obstacle_image = pygame.transform.scale(obstacle_image, (100, 40))
target_image = pygame.transform.scale(target_image,(80,80))


background_color = (255, 255, 255)
background_image = pygame.image.load('background.png')
button_color = (0, 255, 0)


font = pygame.font.Font(None, 36)


game_screen = False  
game_duration = 50  
start_time = 0
score = 0
score_penalty = 0  
penalty_duration = 0.5  
penalty_start_time = 0  


character = pygame.Rect(130, 80, 130, 80)
character_color = (255, 0, 0)
character_speed = 5
target = pygame.Rect(300, 200, 30, 30)
target_color = (255, 255, 0)
obstacles = [pygame.Rect(300, 50, 30, 30), pygame.Rect(300, 150, 30, 30),pygame.Rect(300, 150, 30, 30)]
obstacle_color = (0, 0, 255)
obstacle_speed = [random.randint(5, 13), random.randint(5, 13),random.randint(5, 13)]


start_button = pygame.Rect(450, 350, 100, 50)


game_over_text = font.render("", True, (0, 0, 0))
score_text = font.render("", True, (0, 0, 0))
score_value_text = font.render("", True, (0, 0, 0))
start_button_text = font.render("Start", True, (255, 255, 255))  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_screen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_screen = True
                    start_time = pygame.time.get_ticks()
                    score = 0
                    score_penalty = 0
                    penalty_start_time = 0

    keys = pygame.key.get_pressed()

    if game_screen:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000

        if elapsed_time >= game_duration:
            game_screen = False
            start_time = 0

        if keys[pygame.K_LEFT]:
            character.x -= character_speed
        if keys[pygame.K_RIGHT]:
            character.x += character_speed
        if keys[pygame.K_UP]:
            character.y -= character_speed
        if keys[pygame.K_DOWN]:
            character.y += character_speed

        character.x = max(0, min(screen_width - character.width, character.x))
        character.y = max(0, min(screen_height - character.height, character.y))

        for i in range(len(obstacles)):
            obstacles[i].x -= obstacle_speed[i]

            if obstacles[i].left < 0:
                obstacles[i].left = screen_width
                obstacles[i].top = random.randint(0, screen_height - 30)
                obstacle_speed[i] = random.randint(5, 13)

            if character.colliderect(obstacles[i]) and elapsed_time > penalty_duration and current_time - penalty_start_time >= 500:
                if score_penalty == 0:
                    print("장애물에 닿았습니다!")
                    score -= 50
                score_penalty += 1
                penalty_start_time = current_time

        if character.colliderect(target):
            print("목표지점 도달!")
            score += 100
            target.x = random.randint(0, screen_width - 80)
            target.y = random.randint(0, screen_height - 80)

        screen.blit(background_image, (0, 0))
        screen.blit(character_image, (character.x, character.y))
        screen.blit(target_image, (target.x, target.y))
        for obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle.x, obstacle.y))

        score_text = font.render(f"Score: {score - score_penalty * 50}", True, (0, 0, 0))
        time_text = font.render(f"Time: {game_duration - elapsed_time:.1f} s", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (screen_width - 150, 10))

    else:
        screen.blit(background_image, (0, 0))
        screen.blit(game_over_text, (450, 350))
        score_value_text = font.render(f"총 점수: {score - score_penalty * 50}", True, (0, 0, 0))
        screen.blit(score_value_text, (450, 400))
        pygame.draw.rect(screen, button_color, start_button)
        screen.blit(start_button_text, (start_button.centerx - 30, start_button.centery - 15))
    pygame.display.update()