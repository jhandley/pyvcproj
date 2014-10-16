#!/usr/bin/python

# Fixes the following warning:
#      warning LNK4075: ignoring '/EDITANDCONTINUE' due to '/INCREMENTAL:NO'
#      specification
# Pass in path to solution file.
# For any project that has debug information set to "Edit and Continue"
# This script will set Enable Incremental Linking to true to appease
# the warning.

import vcproj
import os, sys

def main(argv):
  if len(argv) < 2:
      print "Usage: " + argv[0] + " <solution file>"
      sys.exit(2)
  solution_path = argv[1]
  solution_dir = os.path.dirname(solution_path)
  solution = vcproj.solution.parse(solution_path)
  for project_file in solution.project_files():
    project = vcproj.project.parse(os.path.join(solution_dir, project_file))
    if project.configuration_type() != "StaticLibrary":
      # Check for mismatched incr linking and debug format, debug format of None means default which is EditAndContinue
      if project.enable_incremental_linking('Debug', 'Win32') == False and project.debug_information_format('Debug', 'Win32') in ['EditAndContinue', None]:
        print "Set enable incremental to false for " + project_file
        project.set_enable_incremental_linking('Debug', 'Win32', None)
        project.write()

if __name__ == "__main__":
   main(sys.argv)
