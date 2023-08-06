from databricksbundle.container.entryPointContainerLoader import entryPointExists

if entryPointExists():
    from databricksbundle.container.entryPointContainerLoader import readContainerInit # pylint: disable = import-outside-toplevel, unused-import
else:
    from databricksbundle.container.pyprojectContainerLoader import readContainerInit # pylint: disable = import-outside-toplevel, unused-import
