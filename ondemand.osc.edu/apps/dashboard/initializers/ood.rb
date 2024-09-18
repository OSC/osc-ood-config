
def add_paths
  OodFilesApp.candidate_favorite_paths.tap do |paths|
    # add project space directories
    projects = User.new.groups.map(&:name).grep(/^P./)
    
    # add scratch space directories
    paths << Pathname.new("/fs/scratch/#{User.new.name}")
    paths.concat projects.map { |p| Pathname.new("/fs/scratch/#{p}")  }

    paths.concat projects.map { |p| Pathname.new("/fs/ess/#{p}")  }
  end
end

fs_outage = `grep node_file_test_failure /var/lib/node_exporter/textfile_collector/autofs-file-test.prom | grep -q ' 1'; echo $?`
add_paths if fs_outage.chomp == "1" && !File.exist?('/etc/ood/config/gpfs_outage')

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

ENV['OOD_DASHBOARD_HELP_CUSTOM_URL'] = "#{idp}/realms/osc/account/#/security/linked-accounts"

Rails.application.config.after_initialize do
  NavConfig.categories_whitelist=true
end