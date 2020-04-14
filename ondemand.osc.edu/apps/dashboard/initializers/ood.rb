OodFilesApp.candidate_favorite_paths.tap do |paths|
  # add project space directories
  projects = User.new.groups.map(&:name).grep(/^P./)
  paths.concat projects.map { |p| Pathname.new("/fs/project/#{p}")  }

  # add scratch space directories
  paths << Pathname.new("/fs/scratch/#{User.new.name}")
  paths.concat projects.map { |p| Pathname.new("/fs/scratch/#{p}")  }

  # add ess scratch and project directories
  paths.concat projects.map { |p| Pathname.new("/fs/ess/scratch/#{p}")  }
  paths.concat projects.map { |p| Pathname.new("/fs/ess/#{p}")  }
end

NavConfig.categories_whitelist=true

require 'socket'
hostname = Socket.gethostname
case hostname
when /dev/
  idp = 'https://idp-dev.osc.edu'
when /test/
  idp = 'https://idp-test.osc.edu'
else
  idp = 'https://idp.osc.edu'
end
ENV['OOD_DASHBOARD_HELP_CUSTOM_URL'] = "#{idp}/auth/realms/osc/account/identity"
