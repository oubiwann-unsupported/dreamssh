def refresh_plugin_cache():
    print "Refreshing Twisted plugin cache ..."
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))
