Node: merge_varcopes (fsl)
==========================


 Hierarchy : test_wf_3rd_level.merge_varcopes
 Exec ID : merge_varcopes


Original Inputs
---------------


* args : <undefined>
* dimension : t
* environ : {'FSLOUTPUTTYPE': 'NIFTI_GZ'}
* in_files : ['/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-00_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-00_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-01_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-01_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-02_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-02_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-03_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-03_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-04_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-04_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-05_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-05_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-06_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-06_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-07_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-07_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-08_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-08_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-09_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-09_drug-1.nii.gz']
* merged_file : <undefined>
* output_type : NIFTI_GZ
* tr : <undefined>


Execution Inputs
----------------


* args : <undefined>
* dimension : t
* environ : {'FSLOUTPUTTYPE': 'NIFTI_GZ'}
* in_files : ['/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-00_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-00_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-01_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-01_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-02_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-02_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-03_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-03_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-04_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-04_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-05_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-05_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-06_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-06_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-07_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-07_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-08_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-08_drug-1.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-09_drug-0.nii.gz', '/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-09_drug-1.nii.gz']
* merged_file : <undefined>
* output_type : NIFTI_GZ
* tr : <undefined>


Execution Outputs
-----------------


* merged_file : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/merge_varcopes/varcope_sub-00_drug-0_merged.nii.gz


Runtime info
------------


* cmdline : fslmerge -t varcope_sub-00_drug-0_merged.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-00_drug-0.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-00_drug-1.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-01_drug-0.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-01_drug-1.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-02_drug-0.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-02_drug-1.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-03_drug-0.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-03_drug-1.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-04_drug-0.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-04_drug-1.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-05_drug-0.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-05_drug-1.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-06_drug-0.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-06_drug-1.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-07_drug-0.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-07_drug-1.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-08_drug-0.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-08_drug-1.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-09_drug-0.nii.gz /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/data/varcope_sub-09_drug-1.nii.gz
* duration : 0.062011
* hostname : Xiaoqians-MacBook-Pro.local
* prev_wd : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction
* working_dir : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/merge_varcopes


Terminal output
~~~~~~~~~~~~~~~


 


Terminal - standard output
~~~~~~~~~~~~~~~~~~~~~~~~~~


 


Terminal - standard error
~~~~~~~~~~~~~~~~~~~~~~~~~


 


Environment
~~~~~~~~~~~


* COMMAND_MODE : unix2003
* DISPLAY : /private/tmp/com.apple.launchd.AHZjNgULtI/org.xquartz:0
* FSLDIR : /Users/xiaoqianxiao/fsl
* FSLMULTIFILEQUIT : TRUE
* FSLOUTPUTTYPE : NIFTI_GZ
* FSLTCLSH : /Users/xiaoqianxiao/fsl/bin/fsltclsh
* FSLWISH : /Users/xiaoqianxiao/fsl/bin/fslwish
* FSL_LOAD_NIFTI_EXTENSIONS : 0
* FSL_SKIP_GLOBAL : 0
* HDF5_DIR : /opt/homebrew/opt/hdf5
* HOME : /Users/xiaoqianxiao
* HOMEBREW_CELLAR : /opt/homebrew/Cellar
* HOMEBREW_PREFIX : /opt/homebrew
* HOMEBREW_REPOSITORY : /opt/homebrew
* IDEA_INITIAL_DIRECTORY : /
* INFOPATH : /opt/homebrew/share/info:/opt/homebrew/share/info:/opt/homebrew/share/info:
* KMP_DUPLICATE_LIB_OK : True
* LC_CTYPE : UTF-8
* LOGNAME : xiaoqianxiao
* NIPYPE_NO_ET : 1
* OLDPWD : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction
* PATH : /Users/xiaoqianxiao/fsl/share/fsl/bin:/Users/xiaoqianxiao/fsl/bin:/Users/xiaoqianxiao/fsl/share/fsl/bin:/Users/xiaoqianxiao/fsl/bin:/Users/xiaoqianxiao/PycharmProjects/aboutLive/.venv/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/Library/Frameworks/Python.framework/Versions/3.10/bin:/Users/xiaoqianxiao/.pyenv/shims:/Users/xiaoqianxiao/.local/bin:/Users/xiaoqianxiao/abin:/Users/xiaoqianxiao/tool:/Users/xiaoqianxiao/fsl/bin:/Users/xiaoqianxiao/fsl/share/fsl/bin:/Library/Frameworks/Python.framework/Versions/3.12/bin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/opt/X11/bin:/Users/xiaoqianxiao/.fw:/opt/homebrew/opt/python/libexec/bin:/Users/xiaoqianxiao/abin
* PS1 : (.venv) %n@%m %1~ %# 
* PWD : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction
* R_LIBS : /Users/xiaoqianxiao/sw/R-4.3.1
* SHELL : /bin/zsh
* SHLVL : 1
* SSH_AUTH_SOCK : /private/tmp/com.apple.launchd.XAGM6MDQs6/Listeners
* TERM : xterm-256color
* TERMINAL_EMULATOR : JetBrains-JediTerm
* TERM_SESSION_ID : 3fb853ba-2ee0-4f02-b8c2-8e066f815c57
* TMPDIR : /var/folders/63/3j_hstl96w58qx1sdw9czhxr0000gn/T/
* USER : xiaoqianxiao
* VIRTUAL_ENV : /Users/xiaoqianxiao/PycharmProjects/aboutLive/.venv
* VIRTUAL_ENV_PROMPT : (.venv) 
* XPC_FLAGS : 0x0
* XPC_SERVICE_NAME : 0
* _ : /Users/xiaoqianxiao/PycharmProjects/aboutLive/.venv/bin/python3
* __CFBundleIdentifier : com.jetbrains.pycharm
* __CF_USER_TEXT_ENCODING : 0x1F5:0x0:0x0

