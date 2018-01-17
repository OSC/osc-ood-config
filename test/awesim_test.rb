require "test_helper"

class AweSimTest < Minitest::Test
  def setup
    @apps = AWESIM.join("apps")
  end

  %w[dashboard activejobs myjobs files shell bc_desktop].each do |app|
    define_method "test_that_it_configures_#{app}" do
      assert @apps.join(app).directory?
    end
  end

  %w[dashboard activejobs myjobs].each do |app|
    define_method "test_that_#{app}_sets_portal" do
      env = @apps.join(app, "env")
      assert env.file?
      assert_match(/^OOD_PORTAL="awesim"$/, env.read)
    end

    define_method "test_that_#{app}_sets_dashboard_title" do
      env = @apps.join(app, "env")
      assert env.file?
      assert_match(/^OOD_DASHBOARD_TITLE="AweSim Apps"$/, env.read)
    end
  end
end
