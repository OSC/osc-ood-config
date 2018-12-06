OodFilesApp.candidate_favorite_paths.tap do |paths|
  # add project space directories
  projects = User.new.groups.map(&:name).grep(/^P./)
  paths.concat projects.map { |p| Pathname.new("/fs/project/#{p}")  }

  # add scratch space directories
  paths << Pathname.new("/fs/scratch/#{User.new.name}")
  paths.concat projects.map { |p| Pathname.new("/fs/scratch/#{p}")  }
end

NavConfig.categories_whitelist=true

# don't show develop dropdown unless you are setup for app development
#
# FIXME: this should work if the PUN tells the dashboard what the app schema is
# Configuration.app_development_enabled = DevRouter.base_path.directory?
#
# HACK: workaround for new nginx_config default
# Several problems
#   1. We want the real path to be used, that is ~/ondemand/dev when ssh etc.
#   2. We want the configured path (i.e. local disk) to be used when determining if a user should have access
#
#   The short answer is to maintain the status quo
Configuration.app_development_enabled = File.directory? "/var/www/ood/apps/dev/#{OodSupport::Process.user.name}/gateway"
