Rails.application.configure do |config|
  ActiveSupport.on_load(:active_record) do
    Workflow.where(batch_host: 'pitzer-exp').update_all(batch_host: 'pitzer')
  end
end

