def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def draw_score(screen, score, score_images, SCREEN_WIDHT):
    score_str = str(score)
    for i, digit in enumerate(score_str):
        digit_image = score_images[int(digit)]
        screen.blit(digit_image, (SCREEN_WIDHT // 2 + i * digit_image.get_width(), 50))