from PPlay import sprite


class SpaceShip(sprite.Sprite):

    def __init__(self, imageFile, shoot_cooldown=1, speed=70):
        sprite.Sprite.__init__(self, imageFile)

        self.shouldDraw = True
        self.iFrames = 0.2
        self.iFramesBase = 0.2
        self.stunTimer = 0

        self.shoot_cooldown_base = shoot_cooldown
        self.shoot_cooldown = 0

        self.speed = speed
        self.canMove = True

    def canShoot(self):
        return self.shoot_cooldown <= 0

    def resetShootCooldown(self):
        self.shoot_cooldown = self.shoot_cooldown_base

    def gotHit(self):
        self.stunTimer = 2
        self.canMove = False
        self.shouldDraw = False

    def updateShip(self, deltaTime):
        self.shoot_cooldown -= deltaTime

        if not self.canMove:
            self.stunTimer -= deltaTime

            self.iFrames -= deltaTime
            if self.iFrames <= 0:
                self.shouldDraw = not self.shouldDraw
                self.iFrames = self.iFramesBase

            if self.stunTimer <= 0:
                self.canMove = True

                self.shouldDraw = True
                self.iFrames = self.iFramesBase
