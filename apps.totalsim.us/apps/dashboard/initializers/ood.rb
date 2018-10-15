# hide all menu options
NavConfig.categories = []
NavConfig.categories_whitelist=true if NavConfig.respond_to?(:categories_whitelist=)

# enable dev mode for all configured app developers
Configuration.app_development_enabled = UsrRouter.base_path.directory?
Configuration.app_sharing_facls_enabled = true
