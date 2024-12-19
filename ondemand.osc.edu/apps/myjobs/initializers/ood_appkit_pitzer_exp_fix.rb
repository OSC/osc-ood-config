Rails.application.config.after_initialize do
  Rails.application.configure do |config|
    ActiveSupport.on_load(:active_record) do
      Workflow.where(batch_host: 'pitzer-exp').update_all(batch_host: 'pitzer')
      Workflow.where(batch_host: 'owens-slurm').update_all(batch_host: 'owens')
    end if Configuration.production_database_path.file?
  end
end
