import pygame

#constants
SCREEN_SIZE = (800, 800)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TILE_SIZE = 40
characters = pygame.sprite.Group()
objects = pygame.sprite.Group()
weapons = pygame.sprite.Group()

class Character(pygame.sprite.Sprite):
    """
    Name: Character
    Usage: for the character (controlable character) movements, the output of the character
    """
    def __init__(self, x, y):
        super().__init__()
        self.width = TILE_SIZE
        self.height = TILE_SIZE * 1.5
        self.image = pygame.image.load("images/RIGHT_IDEL1.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.face = "RIGHT"
        self.change = ""
        self.state = "IDEL"
        self.frame_index = 0
        self.animation_speed = 10
        self.counter = 0
        self.weapon = None
        self.animations = {face: {"IDEL": [pygame.image.load(f"images/{face}_IDEL{i}.png") for i in range(1, 4)], "MOVE": [pygame.image.load(f"images/{face}_MOVE{i}.png") for i in range(1, 7)]} for face in ["LEFT", "RIGHT"]}
        self.animations["WEAPONS"] = {
            weapon_name: {face: {
                        "IDEL": [pygame.image.load(f"images/{face}_{weapon_name}_IDEL{i}.png") for i in range(1, 4)],
                        "MOVE": [pygame.image.load(f"images/{face}_{weapon_name}_MOVE{i}.png") for i in range(1, 7)]
                } for face in ["LEFT"]}for weapon_name in ["SWORD"]}

    """
    Name: move
    Usage: control the charater movement on the screen by detecting the key pressing
    also change the states to MOVE
    """

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.state = "MOVE"
            self.rect.x -= 3
            self.change = "LEFT"
            self.face_change()
        elif keys[pygame.K_d]:
            self.state = "MOVE"
            self.rect.x += 3
            self.change = "RIGHT"
            self.face_change()
        elif keys[pygame.K_w]:
            self.state = "MOVE"
            self.rect.y -= 3
        elif keys[pygame.K_s]:
            self.state = "MOVE"
            self.rect.y += 3
        else:
            if self.state == "MOVE":
                self.frame_index = 0
                self.state = "IDEL"

    """
    Name: animation
    Usage: Play the animation
    """

    def animation(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.face][self.state]):
                self.frame_index = 0
        if self.weapon is not None:
            self.image = pygame.transform.scale(self.animations["WEAPONS"][self.weapon.name][self.face][self.state][self.frame_index], (self.width, self.height))
        else:
            self.image = pygame.transform.scale(self.animations[self.face][self.state][self.frame_index], (self.width, self.height))

    """
    Name: face_change
    Usage: Changing the face the character is facing
    """

    def face_change(self):
        if self.weapon is not None:
            if self.change != self.face:
                self.face = self.change
                self.change = ""
                self.image = pygame.transform.scale(self.animations["WEAPONS"][self.weapon.name][self.face][self.state][self.frame_index + 1], (self.width, self.height))
        else:
            if self.change != self.face:
                self.face = self.change
                self.change = ""
                self.image = pygame.transform.scale(self.animations[self.face][self.state][self.frame_index], (self.width, self.height))

    """
    Name: pick_up_weapond
    Usage: check if the character is collide with the weapon. if yes, then the character will own the weapon
    """

    def pick_up_weapon(self):
        col = pygame.sprite.spritecollide(self, weapons, False)
        if col:
            for w in col:
                w.to_be_own(self)
                self.weapon = w

    """
    Name: attack_setter
    Usage: changing the state outside the class
    """

    def attack_setter(self):
        self.state = "ATTACK"

"""
Name: object
Usage: the objects that can be broke are store in here
"""
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pygame.surface.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 10

    """
    Name: hit
    Usage: deal with the situation that the object got hit by the character
    """
    def hit(self, power):
        self.hp -= power
        if self.hp <= 0:
            self.kill()

"""
Name: Weapon
Usage: the weapon class, allows the weapon to be own and display on the screen. also allowing it to hit items
"""
class Weapons(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rage = 0
        self.power = 0
        self.name = ""
        self.hit = False
        self.own = False
        self.owner = None

    """
    Name: to_be_own
    Usage: setting it to be own by the character
    """
    def to_be_own(self, character):
        self.owner = character
        self.own = True
        self.image.set_alpha(0)

    """
    Name: attack
    Usage: attack things, and check the collidtion of the weapon with other objects. arrows and bullets are a different
    """
    def attack(self):
        self.owner.attacking_setter()
        col = pygame.sprite.spritecollide(self, objects, False)
        for o in col:
            return o, self.power
        return None, 0

    """
    Name: updata_position
    Usage: Make it along side with the character
    """
    def update_position(self):
        if self.own:
            self.rect.x = self.owner.rect.x
            self.rect.y = self.owner.rect.y

    """
    Name: have_owner
    Usage: to see if the weapon is own, to prevent crash
    """
    def have_owner(self):
        if self.owner is not None:
            return True
        return False

"""
Name: Sword
Usage: a sub class of the weapon class, specific modify for the weapon sword
"""
class Sword(Weapons):
    def __init__(self, x, y):
        super().__init__(x, y, "images/sword.png")
        self.rage = 10
        self.power = 10
        self.name = "SWORD"

class Hammer(Weapons):
    def __init__(self, x, y):
        super().__init__(x, y, "images/hammer.png")
        self.rage = 20
        self.power = 20
        self.name = "HAMMER"