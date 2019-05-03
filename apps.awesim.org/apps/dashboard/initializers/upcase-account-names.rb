class OodCore::Job::Script
  def accounting_id
    @accounting_id.upcase if @accounting_id
  end
end