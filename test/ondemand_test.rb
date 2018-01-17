require "test_helper"

class OnDemandTest < Minitest::Test
  def setup
    @apps = ONDEMAND.join("apps")
  end

  def env(app)
    @apps.join(app, "env").tap { |p| assert p.file?, "File not found: #{p}" }
  end

  def test_that_it_configures_apps
    %w[dashboard activejobs myjobs files shell bc_desktop].each do |app|
      assert @apps.join(app).directory?, "No configuration found for #{app}"
    end
  end

  def test_that_apps_do_not_set_portal
    %w[dashboard activejobs myjobs].each do |app|
      refute_match(/OOD_PORTAL/, env(app).read, "Portal does not need to be set for #{app}")
    end
  end

  def test_that_apps_set_dashboard_title
    %w[dashboard activejobs myjobs].each do |app|
      assert_match(/^OOD_DASHBOARD_TITLE="OSC OnDemand"$/, env(app).read, "Dashboard title is not set to 'OSC OnDemand' for #{app}")
    end
  end
end
