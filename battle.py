from random import randrange, choice

class Battle:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def fight(self):
        while not self.outcome():
            (next_actor, isLeft) = self.pick_next_actor()
            effect = next_actor.act(self.battle_view(next_actor, isLeft))
            print(effect)
            self.apply_effect(effect)
            print(self)

    def outcome(self):
        if len(list(filter(lambda f: f.alive(), self.left))) == 0:
            return "Left Dead"
        if len(list(filter(lambda f: f.alive(), self.right))) == 0:
            return "Right Dead"
            
    def actors_on_side(self, isLeft, exclude=None):
        actors = self.left if isLeft else self.right
        if exclude:
            return actors[:].remove(exclude)
        else:
            return actors

    def battle_view(self, actor, isLeft):
        return BattleView(self.actors_on_side(isLeft, exclude=actor), self.actors_on_side(not isLeft))

    def pick_next_actor(self):
        actor = None
        while not actor or not actor.alive():
            num_actors = len(self.left) + len(self.right)
            i = randrange(0,num_actors)
            actor = (self.left + self.right)[i]
            side = i < len(self.left)
        return (actor, side)
    
    def apply_effect(self, effect):
        effect.actor.apply_hit(effect.hit)

    def __str__(self):
        left = list(map(str, self.left))
        right = list(map(str, self.right))
        return " ".join(left) + "  vs  " + " ".join(right)

class BattleView:
    def __init__(self, team, rivals):
        self.team = team
        self.rivals = rivals

class Fighter:
    def __init__(self, level, vitality, strength, damage, defense, chin):
        self.level = level
        self.vitality = vitality
        self.strength = strength
        self.damage = damage
        self.defense = defense
        self.chin = chin
        self.restore()

    def __str__(self):
        return f"{self.life}/{self.max_life()}"

    def act(self, battle_view):
        return Effect(self.max_hit() * 1 * 1, choice(battle_view.rivals))

    def max_hit(self):
        return self.strength * self.level + self.damage

    def alive(self):
        return self.life > 0

    def restore(self):
        self.life = self.max_life()

    def max_life(self):
        return self.level * self.vitality

    def apply_hit(self, hit):
        harm = int(max(0, (hit - 1 * self.level) / (self.defense * 1) - self.chin))
        self.life -= harm
        if self.life <= 0:
            self.life = 0

class Effect:
    def __init__(self, hit, actor):
        self.hit = hit
        self.actor = actor

    def __str__(self):
        return f"Hit {self.hit} on {self.actor}"

if __name__ == "__main__":
    p1 = Fighter(4, 12, 5, 1, 4, 3)
    p2 = Fighter(6, 11, 5, 1, 4, 1)
    slime1 = Fighter(2, 9, 3, 1, 3, 0)
    slime2 = Fighter(2, 9, 3, 1, 3, 0)
    bull = Fighter(4, 14, 4, 1, 4, 1)

    b = Battle([p1, p2], [slime1, slime2, bull])
    b.fight()
