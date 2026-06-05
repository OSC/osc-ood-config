require "test_helper"

class OndemandDTest < Minitest::Test
  def setup
    @ondemand_d_dirs = [
      ONDEMAND.join("ondemand.d"),
      AWESIM.join("ondemand.d"),
      CLASS.join("ondemand.d"),
      TOTALSIM.join("ondemand.d")
    ]
  end

  def test_that_ondemand_d_files_are_same_across_portals
    all_files = @ondemand_d_dirs.map do |dir|
      Dir.glob(dir.join("**", "*")).map { |f| Pathname.new(f) }.select(&:file?).sort
    end

    # Check for missing files by relative path
    rel_files = @ondemand_d_dirs.zip(all_files).map do |dir, files|
      files.map { |f| f.relative_path_from(dir) }
    end

    unique_rel_files = rel_files.flatten.uniq
    missing = []
    unique_rel_files.each do |rel_file|
      @ondemand_d_dirs.each do |dir|
        unless dir.join(rel_file).file?
          missing << dir.join(rel_file)
        end
      end
    end

    assert missing.empty?, "Missing ondemand.d files:\n  #{missing.join("\n  ")}"

    # totalsim's navigation is allowed to be different.
    totalsim_nav = Pathname.new('apps.totalsim.us/ondemand.d/nav_bar.yml')

    # Compare file contents
    all_files.combination(2) do |a_files, b_files|
      a_files.zip(b_files) do |a, b|
        unless a == totalsim_nav || b == totalsim_nav
          assert FileUtils.cmp(a, b), "ondemand.d files differ:\n  #{a}\n  #{b}"
        end
      end
    end
  end
end
