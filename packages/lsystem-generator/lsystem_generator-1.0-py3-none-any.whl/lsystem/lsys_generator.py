import math
import numpy as np
import string
from matplotlib import pyplot as plt
from lsystem.utils import plot2Image

class Lsystem():
    """class for managing Lsystem, declaring axioms, rules for generation, generations and rules for rendering"""
        
    def __init__(self, axiom: str, *rules: list):
        """ 
        Parameters:
            axiom(str): Initial axiom sequence to start with
            rules(list): list of tuples t where t[0] is the axiom t[1] the generation rule for this axiom 
        """
        if any(len(rule) != 2 for rule in rules): raise ValueError('each rule tuple  must be composed of an axiom and a rule for generation as ("F", "F+F")') 
        
        self.axiom = axiom
        self.rules = rules
        self.__sequence = self.axiom 
        self.__generation = 0

    def __reset(self):
        self.__sequence = "".join(self.axiom)
        self.__generation = 0

    def generate(self, generation: int):
        """Generation method

        Parameters:
            generation(int): generation to be produce

        Returns:
            sequence(str): the generated sequence    
        """
        if generation < 0: raise ValueError("generation can't be negative") 
        if generation < self.__generation: self.__reset() 

        try:
            for rule in self.rules: 
                 self.__sequence = self.__sequence.replace(rule[0], rule[1])       
            self.__generation += 1
            # recursive call to generate the next generation
            return self.__sequence if self.__generation == generation else self.generate(generation)
        except Exception as e:
            print("generating generation {} returns error {}".format(self.__generation, e))

    def render(self, *rendering_rules :list):
        """Render lsystem sequence to an image

        Parameters:
            rendering_rules(list): list of tuples t to render the image using the turtle analogy:
                    t[0]: a character in the sequence for which a rotation with the angle t[1] in degrees needs to be applied

        Returns:
            image(Pile.Image): the generated     
        """
        try: 
            #from the sequence calculate coordinates of points to be rendered
            points = self.calculateCoordinates(rendering_rules)
            plt.clf()
            plt.axis("off")
            plt.plot(*points.T, '-')
            return plot2Image(plt)
        except Exception as e:
            print(e)

    def calculateCoordinates(self, rendering_rules :list):
        """Calculate coordinates in a plot using the turtles analogy

        Parameters:
            rendering_rules(list): list of tuples t to render the image using the turtle analogy:
                    t[0]: a character in the sequence for which a rotation with the angle t[1] in degrees needs to be applied

        Returns:
            points(ndarray)     
        """
        if any(len(rule) != 2 for rule in rendering_rules): raise ValueError('each tuple arguments must be composed of an axiom and a rule for generation as ("F", "F+F")')
        points = list()
        points.append([0,0])
        angle = 0
        for s in self.__sequence:
            rule = [rule for rule in rendering_rules if rule[0] == s]
            if rule:
                angle += math.radians(rule[0][1])
            else:
                points.append([
                    points[-1][0] + math.cos(angle),
                    points[-1][1] + math.sin(angle)
                ])
        return np.asarray(points)
    