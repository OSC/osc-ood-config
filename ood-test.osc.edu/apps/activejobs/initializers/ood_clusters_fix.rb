OODClusters = OodCore::Clusters.new(
  OODClusters.reject { |cluster| [:quick_ruby, :quick_pitzer].include?(cluster.id) }
)
