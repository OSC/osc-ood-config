require "test_helper"

class ShellTest < Minitest::Test
  def setup
    @app_roots = [
      ONDEMAND.join("apps", "shell"),
      AWESIM.join("apps", "shell"),
      CLASS.join("apps", "shell")
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
    assert missing.empty?, "Missing Shell App files:\n  #{missing.join("\n  ")}"

    # Compare files
    app_files.combination(2) do |a_files, b_files|
      a_files.zip(b_files) do |a, b|
        unless File.basename(a) == 'env' && File.basename(b) == 'env'
          assert FileUtils.cmp(a, b), "Shell App files differ:\n  #{a}\n  #{b}"
        else
          # FIXME: add a test case for env files
        end
      end
    end
  end
end
