class UsrRouter
  def owner_title
    return @owner_title if defined?(@owner_title)

    @owner_title ||= (Etc.getpwnam(owner).gecos || owner)
  rescue
    @owner_title = owner
  end

  def caption
    if owner_title == owner
      "Shared by #{owner}"
    else
      "Shared by #{owner_title} (#{owner})"
    end
  end
end
