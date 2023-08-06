# pylint: disable = invalid-name
from typing import Tuple, List
from injecta.service.class_.InspectedArgument import InspectedArgument
from databricksbundle.display import display
from databricksbundle.notebook.decorator.argsChecker import checkArgs
from databricksbundle.notebook.decorator.executor.dataFrameLoader import loadDataFrame
from databricksbundle.notebook.decorator.executor.transformation import transform
from databricksbundle.notebook.decorator.executor.dataFrameSaver import saveDataFrame
from databricksbundle.notebook.function.functionInspector import inspectFunction

def _resolveArguments(inspectedArguments: List[InspectedArgument], decoratorArgs: tuple):
    from databricksbundle.notebook.init import argumentsResolver  # pylint: disable = import-outside-toplevel
    return argumentsResolver.resolve(inspectedArguments, decoratorArgs)

def _notebookFunctionExecuted(fun):
    return fun.__module__ == '__main__'

def _resolveSourceFunctions(decoratorArgs: tuple) -> Tuple[callable]:
    sourceFunctions: List[callable] = []

    for decoratorArg in decoratorArgs:
        if callable(decoratorArg):
            sourceFunctions.append(decoratorArg)
        else:
            break

    return tuple(sourceFunctions)

class notebookFunction:

    def __init__(self, *args): # pylint: disable = unused-argument
        self._decoratorArgs: tuple = args
        checkArgs(args, self.__class__.__name__)

    def __call__(self, fun, *args, **kwargs):
        if _notebookFunctionExecuted(fun):
            arguments = _resolveArguments(inspectFunction(fun), self._decoratorArgs)
            fun(*arguments)

        return fun

class dataFrameLoader:

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        self._decoratorArgs: tuple = args
        self._displayEnabled = kwargs.get('display', False)
        checkArgs(args, self.__class__.__name__)

    def __call__(self, fun, *args, **kwargs):
        if _notebookFunctionExecuted(fun):
            arguments = _resolveArguments(inspectFunction(fun), self._decoratorArgs)
            df = loadDataFrame(fun, arguments)

            if self._displayEnabled:
                display(df)

        return fun

class transformation:

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        self._decoratorArgs: tuple = args
        self._displayEnabled = kwargs.get('display', False)
        self._checkDuplicateColumns = kwargs.get('checkDuplicateColumns', True)

    def __call__(self, fun, *args, **kwargs):
        if _notebookFunctionExecuted(fun):
            sourceFunctions = _resolveSourceFunctions(self._decoratorArgs)
            startIndex = len(sourceFunctions)
            arguments = _resolveArguments(inspectFunction(fun)[startIndex:], self._decoratorArgs[startIndex:])
            df = transform(fun, sourceFunctions, arguments)

            if self._checkDuplicateColumns:
                from databricksbundle.notebook.init import duplicateColumnsChecker  # pylint: disable = import-outside-toplevel
                duplicateColumnsChecker.check(df, fun, sourceFunctions)

            if self._displayEnabled:
                display(df)

        return fun

class dataFrameSaver:

    def __init__(self, *args):
        self._decoratorArgs: tuple = args

    def __call__(self, fun, *args, **kwargs):
        if _notebookFunctionExecuted(fun):
            sourceFunctions = _resolveSourceFunctions(self._decoratorArgs)
            startIndex = len(sourceFunctions)
            arguments = _resolveArguments(inspectFunction(fun)[startIndex:], self._decoratorArgs[startIndex:])
            saveDataFrame(fun, sourceFunctions, arguments)

        return fun
