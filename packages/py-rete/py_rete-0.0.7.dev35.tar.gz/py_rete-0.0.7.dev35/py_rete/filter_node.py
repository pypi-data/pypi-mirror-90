import inspect

from py_rete.beta import ReteNode
from py_rete.common import V


class FilterNode(ReteNode):
    """
    A beta network class. Takes a code snipit, replaces variables with bound
    values, executes it. If the code evaluates to True (boolean), then it
    activates the children with the token/wme

    TODO:
        - explore use of functions/partials instead of string code snipits
    """

    def __init__(self, children, parent, tmpl):
        """
        :type children:
        :type parent: BetaNode
        :type bind: str
        """
        super(FilterNode, self).__init__(children=children, parent=parent)
        self.tmpl = tmpl

    def left_activation(self, token, wme, binding=None):
        """
        :type binding: dict
        :type wme: WME
        :type token: Token
        """
        func = self.tmpl
        all_binding = token.all_binding()
        all_binding.update(binding)

        args = inspect.getfullargspec(func)[0]
        args = {arg: all_binding[V(arg)] for arg in args}

        result = func(**args)

        if bool(result):
            for child in self.children:
                child.left_activation(token, wme, binding)
