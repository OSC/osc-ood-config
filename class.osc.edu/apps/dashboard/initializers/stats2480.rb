Rails.application.config.after_initialize do
  def add_paths
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
  end

  fs_outage = `grep node_file_test_failure /var/lib/node_exporter/textfile_collector/autofs-file-test.prom | grep -q ' 1'; echo $?`
  add_paths if fs_outage.chomp == "1" && !File.exist?('/etc/ood/config/gpfs_outage')
end