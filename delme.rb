

base = 'ondemand.osc.edu/apps/myjobs/templates/'
children = Dir.children(base)

children.each do |child|
  if child.to_s.end_with?('Owens')
    
    pitzer_variant = children.include?(child.gsub('Owens', 'Pitzer'))
    puts child unless pitzer_variant
  end
end