import yamlchecker

class TestYAMLChecker:
    def setUp(self):
        self.y = yamlchecker.YAMLChecker("tests/test.yml")

    def testFlatVariable(self):
        assert self.y.get_variable("flat") == "property"

    def testEmptyVariable(self):
        assert self.y.get_variable("empty") is None

    def testNestedVariable(self):
        assert self.y.get_variable("nested 0:nested 1:nested 2") == "property"

    def testVariableNotPresent(self):
        assert self.y.get_variable("not present") is None

    def testNestedVariableNotPresent(self):
        assert self.y.get_variable("nested 3:nested 4") is None


class TestEmptyYAMLChecker:
    def setUp(self):
        print "Ran me"
        self.y = yamlchecker.YAMLChecker("tests/emptytest.yml")


    def testEmpty(self):
        assert self.y.get_variable("any variable") is  None