import pygame
import random
import sys #Принудително завершит работу

clock = pygame.time.Clock() #часы

pygame.init() #инициализация игры
screen = pygame.display.set_mode((1920,960)) #установка размеров игры
pygame.display.set_caption("Pioneer") #Название для окошка
icon = pygame.image.load('Icon/DH.png') #Установка иконки в программу
pygame.display.set_icon(icon) #загрузка иконки в приложение

# --- ШРИФТЫ (Добавляем для надписи проигрыша) ---
font_lose = pygame.font.Font(None, 100) # Шрифт по умолчанию, размер 100
font_restart = pygame.font.Font(None, 50)
text_lose = font_lose.render('GAME OVER', True, (255, 0, 0)) # Красный текст
text_restart = font_restart.render('Press R to restart', True, (255, 255, 255)) # Белый текст
font_ammo = pygame.font.Font(None, 40) #Шрифт для патронов
font_win = pygame.font.Font(None, 100) #Шрифт для победы
text_win = font_win.render('YOU WIN',True,(20,40,20)) #Вывод текста с цветом


laser = pygame.image.load('Icon/LR.png').convert_alpha()
lasers = []
laser_left = pygame.transform.flip(laser, True, False) # Отражаем по горизонтали

#  ПЕРЕМЕННЫЕ ДЛЯ СТРЕЛЬБЫ 
bullets_left = 3        # Текущее количество патронов,переменная следит, чтобы можно было выстрелить только 3 раза.
max_bullets = 3         # Максимум патронов
is_reloading = False    # Идет ли перезарядка,блокирует переменную кол-во патронов,когда идёт перезарядка
RELOAD_EVENT = pygame.USEREVENT + 2 # Создаем событие для таймера перезарядки

font_menu = pygame.font.Font(None,100)
text_menu = font_menu.render('PLAY',True,(0,0,0))
font_title = pygame.font.Font(None,150)
text_title = font_title.render('Pioneer',True,(100,255,100))

font_Themurders = pygame.font.Font(None, 40)

font_EXP = pygame.font.Font(None, 40)

Heart = pygame.image.load('Icon/Heart.png') #Задаём иконку для сердечка
Heart = pygame.transform.scale(Heart,(45,45))#Задаём размеры 
#Создаю босса
boss_img = pygame.image.load('Icon/Boss.png').convert_alpha()
boss_img = pygame.transform.scale(boss_img,(200,200)) #Задаём размеры для модельки босса
boss_hp = 500
boss_active = False
boss_x = 1930
boss_y = 400
boss_speed = 5
boss_direction = 1 
#Пули босса
boss_laser_img = pygame.image.load('Icon/LR.png').convert_alpha()
boss_laser = []
#Таймер стрельбы босса
BOSS_SHOOT_EVENT = pygame.USEREVENT + 3


# Создаем кнопку (Прямоугольник): (x, y, ширина, высота) для уровней сложности
easy_button_rect = pygame.Rect(500, 400, 300, 100)   # Кнопка ЛЕГКО
medium_button_rect = pygame.Rect(1100, 400, 320, 100) # Кнопка СРЕДНЕ
text_easy = font_menu.render('EASY', True, (0, 0, 0)) #Задаём текст
text_medium = font_menu.render('MEDIUM', True, (0, 0, 0)) #Задаём текст
menu_button_rect = pygame.Rect(800,400,300,100) #Кнопка play
text_play = font_menu.render('PLAY',True,(0,0,0))

pl = pygame.image.load('icon/Space.png').convert_alpha() #Вывод фона

Stars = pygame.image.load('Icon/Stars.png').convert_alpha() #Задаём фон для меню
Stars = pygame.transform.scale(Stars,(1920,960))

walk_right =[
    pygame.image.load('Icon/Fd/fd1.png').convert_alpha(),
    pygame.image.load('Icon/Fd/fd2.png').convert_alpha(),
    pygame.image.load('Icon/Fd/fd3.png').convert_alpha(),
    pygame.image.load('Icon/Fd/fd4.png').convert_alpha(),
    pygame.image.load('Icon/Fd/fd5.png').convert_alpha(),
]

walk_left = [
    pygame.image.load('Icon/bk/Bk1.png').convert_alpha(),
    pygame.image.load('Icon/bk/Bk2.png').convert_alpha(),
    pygame.image.load('Icon/bk/Bk3.png').convert_alpha(),
    pygame.image.load('Icon/bk/Bk4.png').convert_alpha(),
    pygame.image.load('Icon/bk/Bk5.png').convert_alpha(),
]


Alien = pygame.image.load('icon/Sp/WALK_1.PNG').convert_alpha()#Создаём переменную,где будет моделька прищельца
Alien_list = []  #создаём список,где будут храниться прищельцы
Alien_x = 1930 #где он буде расположен по x
Alien_flipped = pygame.transform.flip(Alien, True, False) # Пришелец смотрит в другую сторону
player_anim_count = 0 #создаём счётчик,который будет менять изображения в каждой из указанных переменных
pl_x = 0 # задаём перемещение фона

player_speed = 10  #скорость задаём скорость игрока
player_x = 150  # задаём где будет расположен игрок
player_y = 700  #задаём переменную для прыжка

is_jump = False
jump_count = 10 #на семь позиций поднимаем игрока и также опускаем

sc_sounds = pygame.mixer.Sound('Sounds/Sc.mp3')  # запускаем в программе звук
#sc_sounds.play() #при старте игры запускается звук с помощью класса play

lr_sounds = pygame.mixer.Sound('Sounds/Shot.mp3')

Al_sounds = pygame.mixer.Sound('Sounds/Al.mp3')

Al_sounds.set_volume(0.4)

HM_sounds = pygame.mixer.Sound('Sounds/HM.mp3')

Bs_sounds = pygame.mixer.Sound('Sounds/Bs.mp3')

MK_sounds = pygame.mixer.Sound('Sounds/Mk.mp3')

MK_sounds.set_volume(0.2)

sc_sounds.set_volume(0.1)

Alien_timer = pygame.USEREVENT + 1 #Таймер
pygame.time.set_timer(Alien_timer, 5000) #Задаём таймер для прищельца

kill_score = 0 #задаём счётчик убийств игрока

Exp = 0

Difficulty = "EASY" #режим
exp_per_kill = 100 #сколько очков за убийство
win_game = False #выиграл ли игрок или нет
facting_right = True #Куда смотрит игрок(True - вправо,False - влево)

player_lives = 3 #Максимально кол-во жизней

gameplay = False

menu = True

show_difficulty = False  # Флаг: показывать ли выбор сложности

running = True
while running:
    
    # === БЛОК МЕНЮ === 
    if menu:
        sc_sounds.play()
        #screen.fill((20,20,40))
        screen.blit(Stars,(0,0))
        screen.blit(text_title,(750,200))
        mouse_pos = pygame.mouse.get_pos() #Проверяем наведена ли мышка
        if not show_difficulty:
            # Рисуем только кнопку PLAY
            if menu_button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (200, 255, 200), menu_button_rect)
            else:
                pygame.draw.rect(screen, (100, 150, 100), menu_button_rect)
            # Центрирование:
            text_play_rect = text_play.get_rect(center=menu_button_rect.center)#Задаём по центру текст в прямоугольнике
            screen.blit(text_play, text_play_rect)

        else:
          # Кнопка EASY
            if easy_button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (200, 255, 200),easy_button_rect)
            else:
                pygame.draw.rect(screen, (100, 150, 100),easy_button_rect)
          # Центрирование:
            text_easy_rect = text_easy.get_rect(center=easy_button_rect.center) #Задаём по центру текст в прямоугольнике
            screen.blit(text_easy, text_easy_rect)

          # Кнопка MEDIUM
            if medium_button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 200, 200), medium_button_rect)
            else:
                pygame.draw.rect(screen, (150, 100, 100), medium_button_rect)
          # Центрирование:
            text_medium_rect = text_medium.get_rect(center=medium_button_rect.center)#Задаём по центру текст в прямоугольнике
            screen.blit(text_medium, text_medium_rect)
    
        


    # === БЛОК ИГРЫ ===
    elif gameplay:
        sc_sounds.stop()
        if Exp >= 1500:
            gameplay = False
            win_game = True
        screen.blit(pl,(pl_x,0)) #создаём фон
        screen.blit(pl,(pl_x + 1920,0)) #создаём в кадре ещё один фон
        # Проверка: пора ли выпускать босса?
        if Difficulty == "MEDIUM" and Exp >= 1000 and not boss_active:
            boss_active = True
            MK_sounds.play()
            pygame.time.set_timer(BOSS_SHOOT_EVENT, 1500) # Босс будет стрелять каждые 1.5 сек
         # Отображение количества патронов на экране
        if is_reloading:
            ammo_text = font_ammo.render('Reloading...', True, (255, 255, 0)) #Рисуем reloading,если идёт перезарядка
        else:
            ammo_text = font_ammo.render(f'Ammo: {bullets_left}/{max_bullets}', True, (255, 255, 255)) #Если же не идёт,то отображаем кол-во патронов из скольки скольки
        screen.blit(ammo_text, (50, 50)) # Рисуем текст в углу 
        score_text = font_Themurders.render(f'Kills: {kill_score}',True,(255,255,255))
        screen.blit(score_text,(1700,50))
        score_Exp = font_EXP.render(f'Exp: {Exp}',True,(255,255,255))
        screen.blit(score_Exp,(960,50))
        #Рисуем сердечки
        for i in range(player_lives):
            # Рисуем каждое сердечко со смещением по горизонтали
             # 50 + i * 50 означает: первое на 50px, второе на 100px, третье на 150px
             screen.blit(Heart, (50 + i * 50, 100))


        # Создаем квадрат игрока. ВАЖНО: используем topleft для правильной позиции
        player_rect = walk_right[0].get_rect(topleft=(player_x - 60, player_y - 60)) #Рисуем воображаемый квадрат вокруг игрока
        player_rect = player_rect.inflate(-70, -20)
        
        # Отрисовка и логика врагов
        if Alien_list: #Проверяем есть ли элементы в списке
            for index, el in enumerate(Alien_list): #Перебираем эти элементы
                screen.blit(el[2], el[0]) #Для каждого изображения мы рисуем гуманойда,и задаём в тех координатах,которые были указаны в списке
                el[0].x += el[1] #Настолько гуманойд перемещается
                
                # Проверка столкновения прямо здесь для каждого врага
                if player_rect.colliderect(el[0]):
                    player_lives -= 1 #Отнимаем одну жизнь
                    Alien_list.pop(index) #Удаляем прищельца при столкновении с игроком
                    HM_sounds.play()
                    if player_lives <= 0: # Если жизней меньше 1,то смерть
                        gameplay = False # Игрок проиграл
                        win_game = False
        if boss_active:
            #1.Отрисовка босса
            boss_rect = boss_img.get_rect(topleft=(boss_x,boss_y))
            screen.blit(boss_img,boss_rect)
            #2. Вылет босса на экран
            if boss_x > 1500: # Босс вылетает справа и останавливается на позиции 1500
                boss_x -= 2
            #3.Движение вверх вниз
            boss_y += boss_speed * boss_direction
            if boss_y <= 100 or boss_y >= 700:
                boss_direction *= - 1 #Меняем направление при достижении границ

            #4.Полоска здоровья босса над его головой
            pygame.draw.rect(screen,(255,0,0),(boss_x,boss_y - 20, 200,10))#Красный фон
            pygame.draw.rect(screen,(0,255,0),(boss_x,boss_y - 20, boss_hp/5 * 2,10)) #Зелёное хп

        
        keys = pygame.key.get_pressed() #Задаём управление для игрока
        
        # Движение влево
        if keys[pygame.K_a]:
            facting_right = False
            screen.blit(walk_left[player_anim_count],(player_x,player_y))
            if player_x > 50: #Откуда он может бежать с пикселей
                player_x -= player_speed 
                pl_x += 2
                if pl_x == 1900:
                    pl_x = 0
        # Движение вправо
        elif keys[pygame.K_d]:
            facting_right = True #Запоминаем куда смотрит игрок,в какую сторону,чтобы туда и стрелять
            screen.blit(walk_right[player_anim_count],(player_x,player_y))
            if player_x < 1900:
                player_x += player_speed
                pl_x -= 2 #Эффект передвижения заднего фона
                if pl_x == -1900: #С помощью условий проверяем наступил ли следующий фон в кадре
                    pl_x = 0 #обнуляем его,чтобы всё повторялось
        else:
            if facting_right:
                screen.blit(walk_right[0],(player_x,player_y))
            else:
                screen.blit(walk_left[0],(player_x,player_y))
        
        # Прыжок
        if not is_jump: #Проверка на значение переменной
            if keys[pygame.K_SPACE]: #Назначаем клавишу
                is_jump = True #Запускаем прыжок
        else: #Делаем процесс прыжка
            if jump_count >= -10: #Условие будет выполняться до определённого момента
                if jump_count > 0:
                    player_y -= (jump_count**2) / 2
                else:
                    player_y += (jump_count**2) / 2
                jump_count -= 1 #Уменьшаем переменную до еденицы
            else:
                is_jump = False #Прыжок закончен
                jump_count = 10 #Обнуляем до начала

        # Анимация
        # Обновляем кадр только если игрок двигается (нажата A или D)
        if keys[pygame.K_a] or keys[pygame.K_d]: 
            if player_anim_count == 4: # У меня 5 картинок (индексы 0,1,2,3,4)
                player_anim_count = 0
            else:
                player_anim_count += 1
        else:
            player_anim_count = 0  # Если стоим, сбрасываем счетчик на 0


        if lasers: #Проверяем список на наличие элементов
            for i in range(len(lasers) -1,-1,-1): #перебираем все элементы в списке
                el = lasers[i]
                if el[1] > 0:
                    screen.blit(laser,(el[0].x,el[0].y)) #Рисуем лазер на фоне
                else:
                    screen.blit(laser_left,(el[0].x,el[0].y)) #Рисуем лазер на фоне
                el[0].x += el[1] #скорость полёта лазера
                if el[0].x > 1930 or el[0].x < -50: #Если лазер улетает за пределы карты
                    lasers.pop(i) #то мы его удаляем
                    continue
                hit_something = False
                if boss_active and el[0].colliderect(boss_rect):
                    boss_hp -= 20 #Уронтбоссу
                    Bs_sounds.play()
                    lasers.pop(i) #Лазер исчезает при столкновении
                    hit_something = True
                    if boss_hp <= 0:
                        Exp += 1000
                        boss_active = False
                        MK_sounds.stop()
                        win_game = True
                if hit_something: continue # Если попали в босса, пули больше нет, идем к следующей

                if Alien_list: #Проверяем список с прищельцами
                    for (index, alien_el) in enumerate(Alien_list): #Перебираем эти элементы со списка
                        if el[0].colliderect(alien_el[0]): #Если элементы списка лазера соприкасаются с элементами списка прищельцев
                            Alien_list.pop(index) #Удаляем прищельца по индексу,который задали в цикле
                            lasers.pop(i) #Удаляем сам лазер
                            Al_sounds.play()
                            kill_score += 1 #Вставляем сюда счётчик убийств,то есть мы считаем кол-во убитых прищельцев,каждый раз,когда лазер соприкоснулся с моделькой прищельца
                            Exp += 100
                            hit_something =True
                            break

                if hit_something: continue
        if boss_laser:
            for i, b_laser in enumerate(boss_laser):
                screen.blit(boss_laser_img, b_laser)
                b_laser.x -= 15 # Скорость пуль босса
        
        # Проверка столкновения пули босса с игроком
                if b_laser.colliderect(player_rect):
                    player_lives -= 1
                    boss_laser.pop(i)
                    HM_sounds.play()
                    if player_lives <= 0:
                        gameplay = False
                        win_game = False
                        MK_sounds.stop()
        
        # Удаление пули, если улетела за экран
                elif b_laser.x < -50:
                    boss_laser.pop(i)
                
    # === БЛОК ПРОИГРЫША ===
    else:
        screen.fill((0, 0, 0)) # Заливаем экран черным
        if win_game == True:
            screen.blit(text_win,(800,400))
            screen.blit(text_restart, (800, 500))
        else:
            screen.blit(text_lose, (750, 400)) # Выводим текст по центру
            screen.blit(text_restart, (800, 500))
        
        # Логика перезапуска
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]: # Если нажали R 
            MK_sounds.stop()        
            player_lives = 3 #Обновляем жизни
            boss_active = False
            win_game = False
            boss_laser.clear()
            boss_hp = 500
            Exp = 0
            kill_score = 0
            gameplay = False #Пока что сам геймплей отключается
            player_x = 150
            player_y = 700
            menu = True #Возвращаение в меню
            show_difficulty = False #Чтобы снова видеть кнопку плей
            pl_x = 0
            is_jump = False
            jump_count = 10
            Alien_list.clear() # Очищаем список врагов
            lasers.clear() #очищаем снаряды
            #Сбрасываем патроны при рестарте
            bullets_left = 3
            is_reloading = False

    pygame.display.update() 

    for event in pygame.event.get(): #Обращаемся ко всем вохможным вариантам
        if event.type == pygame.QUIT: #Если мы обращаемся к типу закрытия
            running = False #завершается цикл
            #pygame.quit() # то игра закрывается

        if event.type == BOSS_SHOOT_EVENT and boss_active and gameplay:
        # Создаем пулю, которая летит от босса к игроку (влево)
            bullet_rect = boss_laser_img.get_rect(topleft=(boss_x, boss_y + 100))
            bullet_rect = bullet_rect.inflate(-160, -25)
            boss_laser.append(bullet_rect)
            lr_sounds.play()
            
            
            #=== Обработка нажатия в меню === 
        if menu and event.type == pygame.MOUSEBUTTONDOWN: #eсли мышь нажала внутри квадрата кнопки — menu становится False, а gameplay становится True.
            if event.button == 1: # Левая кнопка мыши
                mouse_pos = event.pos
                if not show_difficulty:
                    # Если мы на главном экране меню и нажали PLAY
                    if menu_button_rect.collidepoint(mouse_pos):
                        show_difficulty = True
                else:
                # Если нажали на прямоугольник кнопки
                #Если нажали кнопку EASY
                    if easy_button_rect.collidepoint(mouse_pos):
                        exp_per_kill = 100
                        Difficulty = "EASY"
                        menu = False
                        gameplay = True
                        show_difficulty = False
                #Если нажали кнопку Medium
                    elif medium_button_rect.collidepoint(mouse_pos):
                        exp_per_kill = 50
                        Difficulty = "MEDIUM"
                        menu = False
                        gameplay = True
                        show_difficulty = False

        if event.type == Alien_timer and not boss_active: #Если таймер срабатывает
            if event.type == Alien_timer and gameplay:
                side = "right" # По умолчанию справа
    
    # Если сложность средняя, даем шанс появиться слева
                if Difficulty == "MEDIUM":
                    if random.choice([0, 1]) == 0: # 50% шанс
                        side = "left"
            
                if side == "right":
                # Создаем список: [Прямоугольник, Скорость (-30), Картинка]
                    alien_rect_right = Alien.get_rect(topleft=(1930, 650)).inflate(-70, -50)
                    Alien_list.append([alien_rect_right, -30, Alien])
                else:
                # Спавним слева (координата -50), скорость положительная (+30), картинка перевернутая
                    alien_rect_left = Alien_flipped.get_rect(topleft=(-50, 650)).inflate(-200, -50)
                    Alien_list.append([alien_rect_left, 30, Alien_flipped])
                # Создаем врага, только если игра идет (gameplay == True)
        elif event.type == RELOAD_EVENT:
            bullets_left = max_bullets
            is_reloading = False
            pygame.time.set_timer(RELOAD_EVENT, 0) # Отключаем таймер (0 мс)
            print("Перезарядка завершена!")
        
          #      ЛОГИКА СТРЕЛЬБЫ 
        # Проверяем нажатие КЛАВИШИ отдельно от таймера пришельца
        elif event.type == pygame.KEYUP: #По одному клику - одна пуля
            # Клавиша F для выстрела (можно заменить на pygame.K_k)
            if event.key == pygame.K_f and gameplay:
                lr_sounds.play()
                # Если есть патроны и нет перезарядки
                if bullets_left > 0 and not is_reloading:
                    if facting_right:
                        bullet_speed = 20
                        bullet_x = player_x + 40
                    else:
                        bullet_speed = -20
                        bullet_x = player_x - 40
                    #lasers.append([laser.get_rect(topleft=(bullet_x, player_y + 20)), bullet_speed])
                    new_laser_rect = laser.get_rect(topleft=(bullet_x, player_y + 20)).inflate(-200, -25)
                    lasers.append([new_laser_rect, bullet_speed])
                    bullets_left -= 1
                    print(f"Выстрел! Осталось патронов: {bullets_left}")

                    # Если патроны кончились, запускаем перезарядку
                    if bullets_left == 0:
                        is_reloading = True
                        print("Перезарядка... (3 секунды)")
                        pygame.time.set_timer(RELOAD_EVENT, 3000) # 3000 мс = 3 секунды
    clock.tick(20)#ФПС

pygame.quit()
sys.exit()
    