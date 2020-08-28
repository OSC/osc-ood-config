require "test_helper"

class ClassTest < Minitest::Test
  def setup
    @apps = CLASS.join("apps")
  end

  def env(app)
    @apps.join(app, "env").tap { |p| assert p.file?, "File not found: #{p}" }
  end

  def test_that_it_configures_apps
    %w[dashboard shell bc_osc_jupyter bc_osc_rstudio_server].each do |app|
      assert @apps.join(app).directory?, "No configuration found for #{app}"
    end
  end

  def test_that_apps_do_not_set_portal
    %w[dashboard].each do |app|
      refute_match(/OOD_PORTAL/, env(app).read, "Portal does not need to be set for #{app}")
    end
  end
end
