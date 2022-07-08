from PPlay.window import *
from PPlay.gameimage import *
from spaceShip import SpaceShip
from Monster import *
import MotaUtils

janela = Window(800, 800)
windowColor = (30, 30, 30)

teclado = Window.get_keyboard()
mouse = Window.get_mouse()

dificuldade = 2

open("ranking.txt", "a+")

def playGame(janela, teclado, mouse, dificuldade):

    spaceShip = SpaceShip("images/spaceShip.png",
                          shoot_cooldown=0.4 * dificuldade,
                          speed=MotaUtils.interpolate(dificuldade, 1, 3, 350, 150))

    spaceShip.set_position(janela.width / 2 - spaceShip.width / 2,
                           janela.height - spaceShip.height - 25)

    projectiles = []
    projectile_speed = MotaUtils.interpolate(dificuldade, 1, 3, -500, -250)

    Monster.velX = MotaUtils.interpolate(dificuldade, 1, 3, 100, 200)
    matrizAliens = MonsterMatrix(4, 5)
    matrizAliens.setPositions(janela)
    matrizAliens.updateSize()

    enemyProjectiles = []

    score = 0
    killScore = 150
    totalTime = 0
    HP = 3

    frameCounter = 0
    timeCounter = 0
    fps = ""

    while True:
        janela.set_background_color(windowColor)

        # region Manage Ship
        if spaceShip.canMove:
            if teclado.key_pressed("right") or teclado.key_pressed("D"):
                if spaceShip.x + spaceShip.width < janela.width:
                    spaceShip.move_x(spaceShip.speed * janela.delta_time())
            elif teclado.key_pressed("left") or teclado.key_pressed("A"):
                if spaceShip.x > 0:
                    spaceShip.move_x(-spaceShip.speed * janela.delta_time())

            if teclado.key_pressed("space"):
                if spaceShip.canShoot():
                    projectile = Projectile("images/spaceShipProjectile.png")
                    projectile.set_position(spaceShip.x + spaceShip.width / 2 - projectile.width / 2, spaceShip.y - projectile.height - 5)
                    projectiles.append(projectile)

                    spaceShip.resetShootCooldown()

        if teclado.key_pressed("ESC"):
            youLoseScreen(janela, teclado, mouse, score)
            break

        spaceShip.updateShip(janela.delta_time())

        # endregion

        # region Manage Projectiles

        for projectile in projectiles:
            projectile.move_y(projectile_speed * janela.delta_time())

            if projectile.y <= matrizAliens.baixo:
                if projectile.x + projectile.width >= matrizAliens.esq:
                    if projectile.x <= matrizAliens.dir:
                        if projectile.y + projectile.height >= matrizAliens.cima:

                            for linha in reversed(matrizAliens.monsters):
                                for monster in linha:
                                    if not monster.dead:
                                        if projectile.collided(monster):
                                            projectile.y = -100
                                            if monster.takeDamage():
                                                Monster.velX *= 1.05
                                                if monster.boss == True:
                                                    score += 2*killScore
                                                else:
                                                    score += killScore

            if projectile.y < -10:
                projectiles.remove(projectile)

        # endregion

        # region Manage Aliens

        if matrizAliens.aliveMonsters > 0:
            matrizAliens.outOfBoundsHandler(janela)
            matrizAliens.moveMonsters(Monster.direction * Monster.velX * janela.delta_time())
            newEnemyProj = matrizAliens.randomMonsterShoot()
            if newEnemyProj:
                enemyProjectiles.append(newEnemyProj)
            matrizAliens.shootingTimer -= janela.delta_time()
        else:
            matrizAliens.setPositions(janela)
            dificuldade += 0.2
            Monster.velX = MotaUtils.interpolate(dificuldade, 1, 3, 100, 200)
            matrizAliens.shootingCD *= 0.95



        for projectile in enemyProjectiles:
            projectile.move_y(150 * janela.delta_time())

            if projectile.collided(spaceShip):
                projectile.y = janela.height + 30
                if spaceShip.canMove:
                    HP -= 1
                    spaceShip.gotHit()
                    spaceShip.x = janela.width / 2 - spaceShip.width / 2

            if projectile.y > janela.height + 20:
                enemyProjectiles.remove(projectile)

        # endregion

        # region Manage Systems
        totalTime += janela.delta_time()
        totalTime = min(totalTime, 100)
        killScore = int(MotaUtils.interpolate(totalTime, 0, 100, 150, 50) * 0.33 * dificuldade)

        janela.draw_text("SCORE: " + str(score), 0, 0, bold=True, color=(255, 255, 255), size=36)

        if HP <= 0:
            youLoseScreen(janela, teclado, mouse, score)
            break

        if matrizAliens.baixo >= spaceShip.y:
            youLoseScreen(janela, teclado, mouse, score)
            break

        janela.draw_text("HP: " + str(HP), janela.width - 120, 0, bold=True, color=(255,255,255), size=36)

        frameCounter += 1
        timeCounter += janela.delta_time()

        if timeCounter >= 0.2:
            fps = str(int(frameCounter / timeCounter))
            frameCounter = 0
            timeCounter = 0

        janela.draw_text("FPS: " + fps, 0, 35, bold=True, color=(255, 255, 255), size=20)
        # endregion

        # region Draw Objects

        for projectile in projectiles:
            projectile.draw()

        for projectile in enemyProjectiles:
            projectile.draw()

        matrizAliens.drawMonsters()

        if spaceShip.shouldDraw:
            spaceShip.draw()
        janela.update()

        # endregion

def youLoseScreen(janela, teclado, mouse, score):
    esc_clicked = True

    submitButton = GameImage(image_file="images/button.png")
    submitButton.set_position(janela.width / 2 - submitButton.width / 2, janela.height*0.75)

    while True:
        janela.set_background_color(windowColor)

        submitButton.draw()
        janela.draw_text("Submit", janela.width / 2 - submitButton.width / 2 + 69, janela.height*0.75 + 35, bold=True, color=(255, 255, 255), size=48)

        janela.draw_text("Voce Perdeu!", janela.width/2 - 200, janela.height/2 - 30, bold=True, color=(255, 255, 255), size=48)
        janela.draw_text("Score: " + str(score), janela.width/2 - 200, janela.height/2 + 30, bold=True, color=(255, 255, 255), size=24)
        janela.draw_text("Digite seu nome no console: ", janela.width / 2 - 200, janela.height / 2 + 90, bold=True,
                         color=(255, 255, 255), size=24)

        if mouse.is_button_pressed(1):
            if mouse.is_over_object(submitButton):
                with open("ranking.txt", "a+") as file:
                    nome = input("Digite seu nome aqui: ")
                    file.write("\n" + nome + " " + str(score))
                    print("Score salvo!\nPode voltar para o jogo!")
                file.close()

                break

        if not esc_clicked:
            if teclado.key_pressed("ESC"):
                break

        if not teclado.key_pressed("ESC"):
            esc_clicked = False

        janela.update()

def diffMenu(janela, teclado, mouse):
    buttons = []
    buttons_spacing = 0
    for i in range(3):
        buttons.append(GameImage("images/button.png"))
        buttons[i].set_position(janela.width / 2 - buttons[i].width / 2, 150 + buttons_spacing)
        buttons_spacing += buttons[i].height + 20

    textos = ["Facil", "Médio", "Díficil"]

    clicado = True
    global dificuldade

    while True:
        janela.set_background_color(windowColor)

        selected = False

        for i in range(len(buttons)):
            buttons[i].draw()
            janela.draw_text(textos[i], buttons[i].x + 30, buttons[i].y + buttons[i].height / 2 - 22, size=36,
                             color=(255, 255, 255))

        if mouse.is_button_pressed(1):
            if not clicado:
                clicado = True

                if mouse.is_over_object(buttons[0]):
                    dificuldade = 1
                    selected = True

                elif mouse.is_over_object(buttons[1]):
                    dificuldade = 2
                    selected = True

                elif mouse.is_over_object(buttons[2]):
                    dificuldade = 3
                    selected = True
        else:
            clicado = False

        janela.update()

        if selected or teclado.key_pressed("ESC"):
            break

def rankingMenu(janela, teclado, mouse):

    placar = []

    with open("ranking.txt", "r+") as file:
        for line in file:
            placar.append(line.split())

    try:
        placar.sort(key = lambda x: int(x[1]), reverse=True)

        pontos = []
        for i in range(min(5, len(placar))):
            pontos.append(placar[i][0] +": " +  placar[i][1])
    except:
        pontos = []
        for i in range(5):
            pontos.append("ERROR RNK FILE : ?")

    voltar_button = GameImage("images/button.png")
    voltar_button.set_position(250, 625)

    while True:
        janela.set_background_color(windowColor)

        for i in range(min(5, len(pontos))):
            janela.draw_text(pontos[i], 250, 75+80*i, size=48, bold=True, color=(255,255,255))

        voltar_button.draw()
        janela.draw_text("Voltar", voltar_button.x + 30, voltar_button.y + voltar_button.height / 2 - 22, size=36,
                         color=(255, 255, 255))

        if mouse.is_over_object(voltar_button):
            if mouse.is_button_pressed(1):
                break


        janela.update()

        if teclado.key_pressed("ESC"):
            break

def quitGame(janela):
    janela.close()
    return

def menu(janela, mouse, teclado):
    buttons = []
    buttons_spacing = 0
    for i in range(4):
        buttons.append(GameImage("images/button.png"))
        buttons[i].set_position(janela.width / 2 - buttons[i].width / 2, 150 + buttons_spacing)
        buttons_spacing += buttons[i].height + 20

    textos = ["Play", "Dificuldade", "Ranking", "Sair"]

    clicado = False
    esc_clicked = True

    while True:
        janela.set_background_color(windowColor)

        for i in range(len(buttons)):
            buttons[i].draw()
            janela.draw_text(textos[i], buttons[i].x + 30, buttons[i].y + buttons[i].height / 2 - 22, size=36,
                             color=(255, 255, 255))

        if mouse.is_button_pressed(1):
            if not clicado:
                clicado = True

                if mouse.is_over_object(buttons[0]):
                    playGame(janela, teclado, mouse, dificuldade)
                elif mouse.is_over_object(buttons[1]):
                    diffMenu(janela, teclado, mouse)
                elif mouse.is_over_object(buttons[2]):
                    rankingMenu(janela, teclado, mouse)
                elif mouse.is_over_object(buttons[3]):
                    quitGame(janela)
        else:
            clicado = False

        janela.update()

# Game:
menu(janela, mouse, teclado)
