import sys
import os
import maya.cmds as cmds

def install(userSetup_file, install_dir):

    installation_name = 'mayaseed'

    print 'adding paths for {0} to {1}'.format(installation_name, install_dir)

    file = open(userSetup_file, 'r')
    file_contents = file.read()
    file.close()
    file = open(userSetup_file, 'w')

    inside_block = False
    for line in file_contents.split('\n'):
      if line[:len(installation_name) + 3] == '// ' + installation_name:
        if inside_block:
          inside_block = False
        else:
          inside_block = True
      if not inside_block:
        if not line[:len(installation_name) + 3] == '// ' + installation_name:
            file.write(line + '\n')

    if ((sys.platform == 'win32') or (sys.platform == 'win64')):

      file.write('\n')
      file.write('\n')
      file.write('// ' + installation_name + '  -------------------------------------------------------------------------------\n')
      file.write('\n')
      file.write('$env_script_path = `getenv MAYA_SCRIPT_PATH`;\n')
      file.write('$env_plugin_path = `getenv MAYA_PLUG_IN_PATH`;\n')
      file.write('putenv MAYA_SCRIPT_PATH ($env_script_path + \";' + os.path.join('{0}/'.format(install_dir), 'scripts') +  '\");\n')
      file.write('$env_script_path = `getenv MAYA_SCRIPT_PATH`;\n')


      file.write('putenv MAYA_SCRIPT_PATH ($env_script_path + \";' + os.path.join('{0}/'.format(install_dir), 'graphics') + '\");\n')
      file.write('putenv MAYA_PLUG_IN_PATH ($env_plugin_path + \";' + os.path.join('{0}/'.format(install_dir), 'plugins') + '\");\n')
      file.write('\n')
      file.write('// ' + installation_name + '  -------------------------------------------------------------------------------\n')

      file.close()


    else:

      file.write('\n')
      file.write('\n')
      file.write('// ' + installation_name + '  -------------------------------------------------------------------------------\n')
      file.write('\n')
      file.write('$env_script_path = `getenv MAYA_SCRIPT_PATH`;\n')
      file.write('$env_plugin_path = `getenv MAYA_PLUG_IN_PATH`;\n')
      file.write('putenv MAYA_SCRIPT_PATH ($env_script_path + \":' + os.path.join('{0}/'.format(install_dir), 'scripts') + '\");\n')
      file.write('$env_script_path = `getenv MAYA_SCRIPT_PATH`;\n')
      file.write('putenv MAYA_SCRIPT_PATH ($env_script_path + \":' + os.path.join('{0}/'.format(install_dir), 'graphics') + '\");\n')

      file.write('putenv MAYA_PLUG_IN_PATH ($env_plugin_path + \":' + os.path.join('{0}/'.format(install_dir), 'plugins') + '\");\n')
      file.write('\n')
      file.write('// ' + installation_name + '  -------------------------------------------------------------------------------\n')

      file.close()

    cmds.confirmDialog(title=installation_name + ' install', message='All done!, just restart and enable and plugins not already enabled in the plugin manager. jt', button='OK')
