require 'ood_core/job/adapters/kubernetes'
require 'ood_core/job/adapters/kubernetes/helper'

# monkey patch until https://github.com/OSC/ood_core/pull/778 is released
class OodCore::Job::Adapters::Kubernetes::Helper
  def secret_info_from_json(json_data)
    data = json_data.to_h[:data] || {}

    info = data.symbolize_keys.each_with_object({}) do |data_kv, hash|
      hash[data_kv[0]] = Base64.decode64(data_kv[1])
    rescue
      next
    end
    { ood_connection_info: info }
  end
end