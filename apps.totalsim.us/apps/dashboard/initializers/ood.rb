Rails.application.config.after_initialize do

  # enable dev mode for all configured app developers
  Configuration.app_development_enabled = UsrRouter.base_path.directory?
  Configuration.app_sharing_facls_enabled = true
end
