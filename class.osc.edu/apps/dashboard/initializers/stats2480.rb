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
