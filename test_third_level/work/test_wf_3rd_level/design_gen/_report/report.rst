Node: design_gen (utility)
==========================


 Hierarchy : test_wf_3rd_level.design_gen
 Exec ID : design_gen


Original Inputs
---------------


* base_dir : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/output/design_files
* function_str : def create_mixed_design_files(group_info, base_dir):
    import numpy as np
    import os
    n_subjects = len(group_info)
    n_measures = 2

    # Design matrix: drug effect only
    design = np.zeros((n_subjects * n_measures, 1))
    design[::2, 0] = 1  # Drug condition 1
    design[1::2, 0] = -1  # Drug condition 2

    # Contrast: test drug effect
    con = np.array([1])

    # Dummy cov_split_file: all in one group
    grp = np.ones(n_subjects * n_measures)

    # Save to files
    design_file = os.path.join(base_dir, 'design.mat')
    con_file = os.path.join(base_dir, 'contrast.con')
    grp_file = os.path.join(base_dir, 'design.grp')

    # Save design matrix in FSL .mat format
    with open(design_file, 'w') as f:
        f.write('/NumWaves {}\n'.format(design.shape[1]))
        f.write('/NumPoints {}\n'.format(design.shape[0]))
        f.write('/Matrix\n')
        np.savetxt(f, design, fmt='%.6f')

    # Save contrast in FSL .con format
    with open(con_file, 'w') as f:
        f.write('/ContrastName1 DrugEffect\n')
        f.write('/NumWaves {}\n'.format(len(con)))
        f.write('/NumContrasts 1\n')
        f.write('/Matrix\n')
        np.savetxt(f, [con], fmt='%.6f')

    # Save dummy group file in FSL .grp format
    with open(grp_file, 'w') as f:
        f.write('/NumWaves 1\n')
        f.write('/NumPoints {}\n'.format(len(grp)))
        f.write('/Matrix\n')
        np.savetxt(f, grp, fmt='%d')

    return design_file, con_file, grp_file

* group_info : [('sub-00', 1), ('sub-01', 1), ('sub-02', 1), ('sub-03', 1), ('sub-04', 1), ('sub-05', 2), ('sub-06', 2), ('sub-07', 2), ('sub-08', 2), ('sub-09', 2)]


Execution Inputs
----------------


* base_dir : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/output/design_files
* function_str : def create_mixed_design_files(group_info, base_dir):
    import numpy as np
    import os
    n_subjects = len(group_info)
    n_measures = 2

    # Design matrix: drug effect only
    design = np.zeros((n_subjects * n_measures, 1))
    design[::2, 0] = 1  # Drug condition 1
    design[1::2, 0] = -1  # Drug condition 2

    # Contrast: test drug effect
    con = np.array([1])

    # Dummy cov_split_file: all in one group
    grp = np.ones(n_subjects * n_measures)

    # Save to files
    design_file = os.path.join(base_dir, 'design.mat')
    con_file = os.path.join(base_dir, 'contrast.con')
    grp_file = os.path.join(base_dir, 'design.grp')

    # Save design matrix in FSL .mat format
    with open(design_file, 'w') as f:
        f.write('/NumWaves {}\n'.format(design.shape[1]))
        f.write('/NumPoints {}\n'.format(design.shape[0]))
        f.write('/Matrix\n')
        np.savetxt(f, design, fmt='%.6f')

    # Save contrast in FSL .con format
    with open(con_file, 'w') as f:
        f.write('/ContrastName1 DrugEffect\n')
        f.write('/NumWaves {}\n'.format(len(con)))
        f.write('/NumContrasts 1\n')
        f.write('/Matrix\n')
        np.savetxt(f, [con], fmt='%.6f')

    # Save dummy group file in FSL .grp format
    with open(grp_file, 'w') as f:
        f.write('/NumWaves 1\n')
        f.write('/NumPoints {}\n'.format(len(grp)))
        f.write('/Matrix\n')
        np.savetxt(f, grp, fmt='%d')

    return design_file, con_file, grp_file

* group_info : [('sub-00', 1), ('sub-01', 1), ('sub-02', 1), ('sub-03', 1), ('sub-04', 1), ('sub-05', 2), ('sub-06', 2), ('sub-07', 2), ('sub-08', 2), ('sub-09', 2)]


Execution Outputs
-----------------


* con_file : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/output/design_files/contrast.con
* design_file : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/output/design_files/design.mat
* grp_file : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/output/design_files/design.grp


Runtime info
------------


* duration : 0.001842
* hostname : Xiaoqians-MacBook-Pro.local
* prev_wd : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction
* working_dir : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction/test_third_level/work/test_wf_3rd_level/design_gen


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
* PATH : /Users/xiaoqianxiao/PycharmProjects/aboutLive/.venv/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/Library/Frameworks/Python.framework/Versions/3.10/bin:/Users/xiaoqianxiao/.pyenv/shims:/Users/xiaoqianxiao/.local/bin:/Users/xiaoqianxiao/abin:/Users/xiaoqianxiao/tool:/Users/xiaoqianxiao/fsl/bin:/Users/xiaoqianxiao/fsl/share/fsl/bin:/Library/Frameworks/Python.framework/Versions/3.12/bin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/opt/X11/bin:/Users/xiaoqianxiao/.fw:/opt/homebrew/opt/python/libexec/bin:/Users/xiaoqianxiao/abin
* PS1 : (.venv) %n@%m %1~ %# 
* PWD : /Users/xiaoqianxiao/PycharmProjects/vicarious_fear_extinction
* R_LIBS : /Users/xiaoqianxiao/sw/R-4.3.1
* SHELL : /bin/zsh
* SHLVL : 1
* SSH_AUTH_SOCK : /private/tmp/com.apple.launchd.XAGM6MDQs6/Listeners
* TERM : xterm-256color
* TERMINAL_EMULATOR : JetBrains-JediTerm
* TERM_SESSION_ID : 73a5b4eb-8ae7-4f9c-89d8-580c54809075
* TMPDIR : /var/folders/63/3j_hstl96w58qx1sdw9czhxr0000gn/T/
* USER : xiaoqianxiao
* VIRTUAL_ENV : /Users/xiaoqianxiao/PycharmProjects/aboutLive/.venv
* VIRTUAL_ENV_PROMPT : (.venv) 
* XPC_FLAGS : 0x0
* XPC_SERVICE_NAME : 0
* _ : /Users/xiaoqianxiao/PycharmProjects/aboutLive/.venv/bin/python
* __CFBundleIdentifier : com.jetbrains.pycharm
* __CF_USER_TEXT_ENCODING : 0x1F5:0x0:0x0

