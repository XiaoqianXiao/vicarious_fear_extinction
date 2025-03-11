Node: cluster (fsl)
===================


 Hierarchy : test_wf_3rd_level.cluster
 Exec ID : cluster


Original Inputs
---------------


* args : <undefined>
* connectivity : 26
* cope_file : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/merge_copes/cope_sub-00_drug-0_merged.nii.gz
* dlh : 0.333506
* environ : {'FSLOUTPUTTYPE': 'NIFTI_GZ'}
* find_min : False
* fractional : False
* in_file : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/flameo/stats/zstat1.nii.gz
* minclustersize : False
* no_table : False
* num_maxima : <undefined>
* out_index_file : True
* out_localmax_txt_file : True
* out_localmax_vol_file : <undefined>
* out_max_file : <undefined>
* out_mean_file : <undefined>
* out_pval_file : <undefined>
* out_size_file : <undefined>
* out_threshold_file : True
* output_type : NIFTI_GZ
* peak_distance : <undefined>
* pthreshold : 0.05
* std_space_file : <undefined>
* threshold : 2.3
* use_mm : False
* volume : 1000
* warpfield_file : <undefined>
* xfm_file : <undefined>


Execution Inputs
----------------


* args : <undefined>
* connectivity : 26
* cope_file : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/merge_copes/cope_sub-00_drug-0_merged.nii.gz
* dlh : 0.333506
* environ : {'FSLOUTPUTTYPE': 'NIFTI_GZ'}
* find_min : False
* fractional : False
* in_file : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/flameo/stats/zstat1.nii.gz
* minclustersize : False
* no_table : False
* num_maxima : <undefined>
* out_index_file : True
* out_localmax_txt_file : True
* out_localmax_vol_file : <undefined>
* out_max_file : <undefined>
* out_mean_file : <undefined>
* out_pval_file : <undefined>
* out_size_file : <undefined>
* out_threshold_file : True
* output_type : NIFTI_GZ
* peak_distance : <undefined>
* pthreshold : 0.05
* std_space_file : <undefined>
* threshold : 2.3
* use_mm : False
* volume : 1000
* warpfield_file : <undefined>
* xfm_file : <undefined>


Execution Outputs
-----------------


* index_file : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/cluster/zstat1_index.nii.gz
* localmax_txt_file : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/cluster/zstat1_localmax.txt
* localmax_vol_file : <undefined>
* max_file : <undefined>
* mean_file : <undefined>
* pval_file : <undefined>
* size_file : <undefined>
* threshold_file : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/cluster/zstat1_threshold.nii.gz


Runtime info
------------


* cmdline : cluster --connectivity=26 --cope=/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/merge_copes/cope_sub-00_drug-0_merged.nii.gz --dlh=0.3335060000 --in=/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/flameo/stats/zstat1.nii.gz --oindex=/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/cluster/zstat1_index.nii.gz --olmax=/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/cluster/zstat1_localmax.txt --othresh=/Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/cluster/zstat1_threshold.nii.gz --pthresh=0.0500000000 --thresh=2.3000000000 --volume=1000
* duration : 0.051775
* hostname : Xiaoqians-MacBook-Pro.local
* prev_wd : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction
* working_dir : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/cluster


Terminal output
~~~~~~~~~~~~~~~


 


Terminal - standard output
~~~~~~~~~~~~~~~~~~~~~~~~~~


 Cluster Index	Voxels	P	-log10(P)	MAX	MAX X (vox)	MAX Y (vox)	MAX Z (vox)	COG X (vox)	COG Y (vox)	COG Z (vox)	COPE-MAX	COPE-MAX X (vox)	COPE-MAX Y (vox)	COPE-MAX Z (vox)	COPE-MEAN


Terminal - standard error
~~~~~~~~~~~~~~~~~~~~~~~~~


 Warning: An input intended to be a single 3D volume has multiple timepoints. Input will be truncated to first volume, but this functionality is deprecated and will be removed in a future release.


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

