import agentframework as af

import matplotlib.pyplot as plt
import unittest

# Test environment import

environment = af.import_environment()
# plt.imshow(environment)
# plt.show()

# create agents to test
agents = []
a = af.Agent(environment, agents, init_coords=[0,300],sex='m')
b = af.Agent(environment, agents, init_coords=[0,2],sex='f')
c = af.Agent(environment, agents, init_coords=[2,0],sex='f')
agents.extend([a,b,c])

# Test basic attributes of agents
class TestAgent(unittest.TestCase):
    
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
        #Note: a.set_sex() is not an option
    
    def test_get_post_set(self):

        TestAgent.test_set(TestAgent)
        self.assertEqual(50,a.get_x())
        self.assertEqual(60,a.get_y())
        self.assertEqual(20,a.get_store())
        self.assertEqual(10,a.get_pregnancy())
        self.assertEqual(30,a.get_age())
        self.assertEqual('m',a.get_sex())
    
    def test_is_dead(self):
        a.set_age(10)
        self.assertFalse(a.is_dead(max_age=20))
        self.assertTrue(a.is_dead(max_age=5))
    
    def test_increment_age(self):
        a.set_age(1)
        a.increment_age()
        self.assertEqual(2,a.get_age())
    
    def test_perturb(self):
        for _ in range(100):
            # test the mod300 and that is is perturbed
            self.assertLess(af.perturb(300),300)
            self.assertGreater(af.perturb(0),0)

    def test_distance_to(self):

        self.assertEqual(298,a.distance_to(b))
        self.assertEqual(8**0.5,b.distance_to(c))
        
###### Other tests that were performed:

# 1. Made sure that slider values are passed into the run function in model.py 
# 2. Fixed frame number edge cases to make sure first frame was spawn, then move 
#    and eat and mate were in the correct order
# 3. Whether there was need for randomisation of the agents list (as this was causing
#    drawing flickers) - answer is no 
# 4. Made sure 'optimised movement' did not get stuck by addin random movement if this happens 
# 5. Type and value checking was added to the main python scripts and mistakes will be caught by them
# 6. move, eat, and mate were checked against their behaviours in the simulation


# to run the tests without extra text from command line
if __name__ == '__main__':
    unittest.main()