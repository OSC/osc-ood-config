# array_ids is not currently exported automatically from ood_core
require 'ood_core/job/array_ids'
require 'workflows_controller'
require 'workflow'

class Workflow
  MAX_JOB_ARRAY_TASKS = 1000
  def task_count_ok?
    OodCore::Job::ArrayIds.new(job_array_request).ids.size <= Workflow::MAX_JOB_ARRAY_TASKS
  end
end

class WorkflowsController
  # PUT /workflows/1/submit
  # PUT /workflows/1/submit.json
  def submit
    set_workflow

    # We want to allow the user to resubmit a job that has been run or failed. This will destroy all preexisting
    # job records for this workflow when the job is no longer queued or running, which will clear the submitted state.
    if @workflow.submitted? && !@workflow.active?
      @workflow.jobs.destroy_all
    end

    respond_to do |format|
      if ! @workflow.task_count_ok?
        session[:selected_id] = @workflow.id
        format.html { redirect_to workflows_url, alert: "Job array request (#{@workflow.job_array_request}) results in over #{Workflow::MAX_JOB_ARRAY_TASKS} tasks and will not be submitted." }
        format.json { head :no_content }
      elsif @workflow.submitted?
        session[:selected_id] = @workflow.id
        format.html { redirect_to workflows_url, alert: 'Job has already been submitted.' }
        format.json { head :no_content }
      elsif @workflow.submit
        session[:selected_id] = @workflow.id
        format.html { redirect_to workflows_url, notice: 'Job was successfully submitted.' }
        format.json { head :no_content }
      else
        #FIXME: instead of alert with html, better to have alert and alert_error_output on flash
        format.html { redirect_to workflows_url, flash: { alert: 'Failed to submit batch job:', alert_error: @workflow.errors.to_a.join("\n") }}
        format.json { render json: @workflow.errors, status: :internal_server_error }
      end
    end
  end
end
