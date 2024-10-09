Rails.application.config.after_initialize do
  require 'socket'
  hostname = Socket.gethostname

  # TODO: remove when upgrading to 4.0
  unless hostname =~ /dev/
    # hide all menu options
    NavConfig.categories = ['Files']
    NavConfig.categories_whitelist=true
  end

  # enable dev mode for all configured app developers
  Configuration.app_development_enabled = UsrRouter.base_path.directory?
  Configuration.app_sharing_facls_enabled = true
end