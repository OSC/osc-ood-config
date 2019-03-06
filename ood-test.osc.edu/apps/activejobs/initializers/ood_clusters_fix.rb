OodAppkit.clusters = OodCore::Clusters.new(
  OodAppkit.clusters.reject { |cluster| [:quick_ruby, :quick_pitzer].include?(cluster.id) }
)

if defined?(OODClusters)
  OODClusters = OodCore::Clusters.new(OodAppkit.clusters.select(&:job_allow?))
end
