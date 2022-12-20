
def add_paths
  OodFilesApp.candidate_favorite_paths.tap do |paths|
    # add project space directories
    projects = User.new.groups.map(&:name).grep(/^P./)
    
    # Removing /fs/project from list per asana https://app.asana.com/0/1135148780858012/1203345685227840/f
    # paths.concat projects.map { |p| Pathname.new("/fs/project/#{p}")  }

    # add scratch space directories
    paths << Pathname.new("/fs/scratch/#{User.new.name}")
    paths.concat projects.map { |p| Pathname.new("/fs/scratch/#{p}")  }

    # add ess scratch and project directories
    # Removing /fs/ess/scratch from list per asana https://app.asana.com/0/1135148780858012/1203345685227840/f
    # paths.concat projects.map { |p| Pathname.new("/fs/ess/scratch/#{p}")  }

    paths.concat projects.map { |p| Pathname.new("/fs/ess/#{p}")  }
  end
end

fs_outage = `grep node_file_test_failure /var/lib/node_exporter/textfile_collector/autofs-file-test.prom | grep -q ' 1'; echo $?`
add_paths if fs_outage.chomp == "1" && !File.exist?('/etc/ood/config/gpfs_outage')

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
ENV['OOD_DASHBOARD_HELP_CUSTOM_URL'] = "#{idp}/realms/osc/account/identity"
