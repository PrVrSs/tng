"""
Exercise from https://python-3-patterns-idioms-test.readthedocs.io/en/latest/FunctionObjects.html

Implement Chain of Responsibility to create an “expert system” that solves problems by successively trying one solution
after another until one matches. You should be able to dynamically add solutions to the expert system. The test for
solution should just be a string match, but when a solution fits, the expert system should return the appropriate
type of ProblemSolver object. What other pattern/patterns show up here?
"""