require 'ood_support'

require 'nav_config'
NavConfig.categories = ["Files", "Clusters"]
NavConfig.categories_whitelist = true

OodFilesApp.candidate_favorite_paths.tap do |paths|
  # add project space directories
  projects = User.new.groups.map(&:name).grep(/^P./)
  paths.concat projects.map { |p| Pathname.new("/fs/project/#{p}")  }

  # add scratch space directories
  paths << Pathname.new("/fs/scratch/#{User.new.name}")
  paths.concat projects.map { |p| Pathname.new("/fs/scratch/#{p}")  }
end

require 'application_controller'
class ApplicationController
    def usr_apps
      @usr_apps ||= SysRouter.apps.select{|app| app.name == 'bc_osc_rstudio_server'}
    end
end