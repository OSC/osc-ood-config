require "test_helper"

class DesktopTest < Minitest::Test
  def setup
    @app_roots = [
      ONDEMAND.join("apps", "bc_desktop"),
      AWESIM.join("apps", "bc_desktop"),
    ]
  end

  def test_that_it_is_same_across_portals
    app_files = @app_roots.map do |p|
      Dir.glob(p.join("**", "*")).map{|f| Pathname.new(f)}.select(&:file?).sort
    end

    # Check for missing files
    rel_files = @app_roots.zip(app_files).map do |dir, files|
      files.map {|f| f.relative_path_from(dir)}
    end
    missing = (rel_files.reduce(:+) - rel_files.reduce(:&)).uniq.map do |p|
      @app_roots.map { |dir| dir.join(p) }.reject(&:file?)
    end.flatten
    assert missing.empty?, "Missing Desktop App files:\n  #{missing.join("\n  ")}"

    # Compare files
    app_files.combination(2) do |a_files, b_files|
      a_files.zip(b_files) do |a, b|
        assert FileUtils.cmp(a, b), "Desktop App files differ:\n  #{a}\n  #{b}"
      end
    end
  end
end
