require 'ood_support'

require 'nav_config'
NavConfig.categories = ["Files", "Clusters"]
NavConfig.categories_whitelist = true

require 'application_controller'
class ApplicationController
    def usr_apps
      @usr_apps ||= SysRouter.apps.select{|app| app.name == 'bc_example_rstudio'}
    end
end