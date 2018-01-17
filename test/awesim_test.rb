require "test_helper"

class AweSimTest < Minitest::Test
  def setup
    @apps = AWESIM.join("apps")
  end

  def env(app)
    @apps.join(app, "env").tap { |p| assert p.file?, "File not found: #{p}" }
  end

  def test_that_it_configures_apps
    %w[dashboard activejobs myjobs files shell bc_desktop].each do |app|
      assert @apps.join(app).directory?, "No configuration found for #{app}"
    end
  end

  def test_that_apps_set_portal
    %w[dashboard activejobs myjobs].each do |app|
      assert_match(/^OOD_PORTAL="awesim"$/, env(app).read, "Portal is not set to 'awesim' for #{app}")
    end
  end

  def test_that_apps_set_dashboard_title
    %w[dashboard activejobs myjobs].each do |app|
      assert_match(/^OOD_DASHBOARD_TITLE="AweSim Apps"$/, env(app).read, "Dashboard title is not set to 'AweSim Apps' for #{app}")
    end
  end
end
