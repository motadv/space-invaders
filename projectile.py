from PPlay import sprite


class Projectile(sprite.Sprite):
    speed = -300

    def __init__(self, image_path):
        sprite.Sprite.__init__(self, image_path)
