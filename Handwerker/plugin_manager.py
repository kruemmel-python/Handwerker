class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.hooks = {}

    def register_plugin(self, plugin_name, plugin):
        """Registriert ein neues Plugin."""
        self.plugins[plugin_name] = plugin
        print(f'Plugin {plugin_name} registriert.')

    def register_hook(self, hook_name, func):
        """Erlaubt es Plugins, Funktionen als Hooks zu registrieren."""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(func)
        print(f'Hook {hook_name} registriert.')

    def trigger_hook(self, hook_name, *args, **kwargs):
        """Führt alle Funktionen aus, die für einen bestimmten Hook registriert sind."""
        if hook_name in self.hooks:
            for func in self.hooks[hook_name]:
                func(*args, **kwargs)

plugin_manager = PluginManager()
