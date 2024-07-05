locals {
  static_files_paths = fileset(var.files_static, "**")
  static_files_suffix_matches = {
    for p in local.static_files_paths : p => regexall("\\.[^\\.]+\\z", p)
  }
  static_files_suffixes = {
    for p, ms in local.static_files_suffix_matches : p => length(ms) > 0 ? ms[0] : ""
  }
}
