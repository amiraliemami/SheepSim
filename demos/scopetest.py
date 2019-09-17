

global_variable = "global_variable"
print(global_variable + " printed at the module level.")

class GeoPoint():

    class_attribute = "class_attribute"
    print(class_attribute + " printed at the class level.")

    def __init__(self):
 
        global global_variable
        print(global_variable + " printed at the method level.")
 
        print(GeoPoint.class_attribute + " printed at the method level.")
        print(class_attribute + " printed at the method level without class.")
        
        self.instance_variable = "self.instance_variable"
        print(self.instance_variable + " printed at the method level.")

        method_local_variable = "method_local_variable"
        print(method_local_variable + " printed at the method level.")
        
        
        
    def another_method(self):

        # No access to method_local_variable here
        print(method_local_variable + " printed within another method.")
    
