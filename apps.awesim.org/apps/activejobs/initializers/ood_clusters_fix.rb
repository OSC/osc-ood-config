Rails.application.config.after_initialize do
  OodAppkit.clusters = OodCore::Clusters.new(
    OodAppkit.clusters.reject { |cluster| [:quick_pitzer].include?(cluster.id) }
  )

  if defined?(OODClusters)
    OODClusters = OodCore::Clusters.new(OodAppkit.clusters.select(&:job_allow?))
  end
end