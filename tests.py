import agentframework as af

import matplotlib.pyplot as plt
import unittest

# Test environment import

environment = af.import_environment()
plt.imshow(environment)
plt.show()

# Test basic attributes of agents

class TestAgent(unittest.TestCase):
    
    # create agents to test
    agents = []
    a = af.Agent(environment, agents, init_coords=[0,300],sex='m')
    b = af.Agent(environment, agents, init_coords=[300,300],sex='f')
    agents.extend([a,b])

    def test_get(self):
        self.assertEqual(0,a.get_x())
        self.assertEqual(300,a.get_y())
        self.assertEqual(0,a.get_store())
        self.assertEqual(0,a.get_pregnancy())
        self.assertEqual(0,a.get_age())
        self.assertEqual('m',a.get_sex())
        
    def test_set(self):
        a.set_x(50)
        a.set_y(60)
        a.set_store(20)
        a.set_pregnancy(10)
        a.set_age(30)
        #NOTE: a.set_sex() is not an option
    
    def test_get_post_set(self):
        self.assertEqual(50,a.get_x())
        self.assertEqual(60,a.get_y())
        self.assertEqual(20,a.get_store())
        self.assertEqual(10,a.get_pregnancy())
        self.assertEqual(30,a.get_age())
        self.assertEqual('m',a.get_sex())
    
    def test_is_dead(self):
        a.set_age(10)
        self.assertEqual(False,a.is_dead(max_age=20))
        self.assertEqual(True,a.is_dead(max_age=5))
    
    def test_increment_age(self):
        a.set_age(1)
        a.increment_age()
        self.assertEqual(2,a.get_age())
    
    def test_perturb(self):
        for _ in range(100):
            # test the mod300 and that is is perturbed
            self.assertLess(af.perturb(300))
            self.assertGreater(af.perturb(0))

    def test_distance_to(self):
        
        agents = []
        a = af.Agent(environment, agents, init_coords=[0,300],sex='m')
        b = af.Agent(environment, agents, init_coords=[0,2],sex='f')
        c = af.Agent(environment, agents, init_coords=[2,0],sex='f')
        agents.extend([a,b,c])
        
        self.assertEqual(298,a.distance_to(b))
        self.assertEqual(8**0.5,b.distance_to(c))
        
# to run the tests without extra text from command line
if __name__ == '__main__':
    unittest.main()

