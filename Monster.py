import random

from PPlay.sprite import Sprite
from projectile import Projectile


class Monster(Sprite):
    velX = 0
    direction = 1

    def __init__(self, matriz, i, j, boss=False, dead=False):
        if boss:
            Sprite.__init__(self, "images/alienBoss.png", frames=1)
            self.hp = 3
        else:
            Sprite.__init__(self, "images/alien.png", frames=1)
            self.hp = 1

        self.boss = boss
        self.i = i
        self.j = j
        self.matriz = matriz

        self.dead = dead

    def revive(self):
        self.dead = False
        if self.boss:
            Sprite.__init__(self, "images/alienBoss.png", frames=1)
            self.hp = 3
        else:
            Sprite.__init__(self, "images/alien.png", frames=1)
            self.hp = 1

    def die(self):
        self.matriz.onMonsterDeath(self.i, self.j)

    def takeDamage(self):
        self.hp -= 1

        if self.hp == 0:
            self.die()
            return True

        return False

    def shoot(self):
        projectile = Projectile("images/enemyProjectile.png")
        projectile.set_position(
            self.x+self.width/2,
            self.y+self.height
        )
        return projectile


class MonsterMatrix:

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.monsters = []

        self.baixo = 0
        self.esq = 10000
        self.cima = 10000
        self.dir = 0

        self.shootingCD = 1.5
        self.shootingTimer = 0

        self.aliveMonsters = 0

        for i in range(n):
            linha = []
            for j in range(m):
                monstro = Monster(self, i, j)
                linha.append(monstro)
            self.monsters.append(linha)

    def onMonsterDeath(self, i, j):
        self.monsters[i][j].dead = True
        self.aliveMonsters -= 1
        self.updateSize()

    def updateSize(self):

        self.baixo = 0
        self.esq = 10000
        self.cima = 10000
        self.dir = 0

        for linha in self.monsters:
            for monster in linha:
                if not monster.dead:
                    x = monster.x
                    y = monster.y

                    self.esq = min(self.esq, x)
                    self.dir = max(self.dir, x + monster.width)
                    self.cima = min(self.cima, y)
                    self.baixo = max(self.baixo, y + monster.height)

    def setPositions(self, janela):
        bossN = random.randint(0, self.n-1)
        bossM = random.randint(0, self.m-1)

        for i in range(self.n):
            for j in range(self.m):

                self.monsters[i][j].boss = False

                if i == bossN and j == bossM:
                    self.monsters[i][j].boss = True

                self.monsters[i][j].revive()
                self.aliveMonsters += 1

                self.monsters[i][j].set_position(
                    (janela.width - 1.5 * self.monsters[i][j].width * self.m) / 2
                    + j * self.monsters[i][j].width * 1.5,
                    (self.monsters[i][j].height / 2)
                    + i * self.monsters[i][j].height * 1.5)

        self.updateSize()

    def drawMonsters(self):
        for linha in self.monsters:
            for monster in linha:
                if not monster.dead:
                    monster.draw()

    def outOfBoundsHandler(self, janela):
        for linha in self.monsters:
            for monster in linha:
                if not monster.dead:
                    if (monster.x < 0 and Monster.direction < 0) or \
                            (monster.x + monster.width > janela.width and Monster.direction > 0):
                        self.moveDown()
                        Monster.direction *= -1
                        return

    def moveMonsters(self, ammount):
        self.esq += ammount
        self.dir += ammount
        for linha in self.monsters:
            for monster in linha:
                monster.move_x(ammount)

    def moveDown(self):
        self.cima += 47/2
        self.baixo += 47/2
        for linha in self.monsters:
            for monster in linha:
                monster.move_y(monster.height / 2)

    def randomMonsterShoot(self):
        linha = random.choice(self.monsters)
        validLine = False
        for monster in linha:
            if not monster.dead:
                validLine = True
                break

        while not validLine:
            linha = random.choice(self.monsters)
            for monster in linha:
                if not monster.dead:
                    validLine = True
                    break

        monster = random.choice(linha)

        while monster.dead:
            monster = random.choice(linha)

        if self.shootingTimer <= 0:
            self.shootingTimer += self.shootingCD + random.random()
            return monster.shoot()

        return False
