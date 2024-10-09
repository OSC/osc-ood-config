Rails.application.config.after_initialize do
  # array_ids is not currently exported automatically from ood_core
  require 'ood_core/job/array_ids'
  require 'workflow'

  class Workflow
    validate :task_count_may_not_exceed_max_job_array_tasks
    MAX_JOB_ARRAY_TASKS = 1000

    def task_count_may_not_exceed_max_job_array_tasks
      if ! task_count_ok?
        errors.add(:job_array_request, "must result in less than #{Workflow::MAX_JOB_ARRAY_TASKS} tasks.")
      end
    end

    def task_count_ok?
      return true if (job_array_request.nil? || job_array_request.empty?)

      OodCore::Job::ArrayIds.new(job_array_request).ids.size <= Workflow::MAX_JOB_ARRAY_TASKS
    end
  end
end