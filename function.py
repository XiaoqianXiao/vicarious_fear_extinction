#%%
#generate behav file from source file
#%%
import os
import pandas as pd
import glob
from templateflow.api import get as tpl_get
root_dir = '/Users/xiaoqianxiao/projects'
project_name = 'NARSAD'
task_label = "MRI"
data_dir = os.path.join(root_dir, project_name, task_label)
derivatives_folder = os.path.join(data_dir, "derivatives/fmriprep")
behav_dir = os.path.join(data_dir, 'source_data/behav')

#%%
def load_behavioral_events(behav_dir, subject, session, run, task_label):
    total_length = 616.5
    file_pattern = os.path.join(behav_dir, f'sub-{subject}_ses-{session}_run-{run}_*.csv')
    behav_file_path = glob.glob(file_pattern)
    df_behav = pd.read_csv(behav_file_path[0])
    df_behav['rt'] = pd.to_numeric(df_behav['rt'], errors='coerce')
    df_behav.loc[df_behav['rt'].isna(), 'rt'] = 2
    # Rename the columns for clarity
    df = df_behav[['onset_time', 'rt', 'condition_name']]
    df = df.rename(columns={'onset_time': 'onset',
                            'rt': 'duration',
                            'condition_name': 'trial_type', })

    # Compute fixation end times and durations
    fixation_endtime = list(df_behav['onset_time'][1:])
    fixation_endtime.append(total_length)
    fixation_starttime = pd.Series(df_behav['reaction_time'])
    fixation_onsets = round(df_behav['reaction_time'], 2)
    fixation_duration = round((pd.Series(fixation_endtime) - fixation_starttime), 2)
    fixation_trial_type = 'fixation'
    df_fixation = pd.DataFrame({'onset': fixation_onsets,
                                'duration': fixation_duration,
                                'trial_type': fixation_trial_type})
    df_fixation = df_fixation.dropna()
    df_combine = pd.concat([df, df_fixation], axis=0)
    return df_combine
#subjects = ['001','002','003','004']
subjects = ['2001LH']
task_labels = ["selfother"]
sessions = ['Baseline']
runs = ['01', '02']
for subject in subjects:
    for session in sessions:
        for run in runs:
            print(f'sub:{subject}; run:{run}')
            for task_label in task_labels:
                results_dir = os.path.join(data_dir, 'sub-' + subject, 'func')
                result_file_name = f'sub-{subject}_ses-{session}_run-{run}_task-{task_label}_events.tsv'
                result_file_path = os.path.join(results_dir, result_file_name)
                if not os.path.exists(results_dir):
                    os.makedirs(results_dir)
                df = load_behavioral_events(behav_dir, subject, session, run, task_label)
                df.to_csv(result_file_path, sep='\t', index=False)

#%%
#clustering
import os
import subprocess
from nipype.interfaces.fsl import SmoothEstimate


def run_command(command):
    """Execute a shell command and handle errors."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")


def cluster(input_file, threshold, pthreshold, dlh, connectivity, volume, out_index_file, out_threshold_file,
            out_localmax_txt_file):
    """Run FSL's cluster command."""
    command = f"/Users/xiaoqianxiao/fsl/bin/fsl-cluster -i {input_file} -t {threshold} -p {pthreshold} -d {dlh} --connectivity={connectivity} --volume={volume} --oindex={out_index_file} --othresh={out_threshold_file} --olmax={out_localmax_txt_file}"
    run_command(command)


# Define mask file from template
mask_file = tpl_get(entities['space'], resolution=2, desc='brain', suffix='mask')

# Define contrasts
contrast_dic = {
    '1': 'Self_Case',
    '2': 'Other_Case',
    '3': 'Self_Other',
    '4': 'Self_Fixation',
    '5': 'Other_Fixation'
}
contrast_list = list(contrast_dic.keys())

# Third level directory
third_level_dir = "/Users/xiaoqianxiao/Experiment/RO1/selfother/derivatives/fMRI_analysis/thirdlevel_all"

for c in contrast_list:
    zstat_file = os.path.join(third_level_dir, f'cope-{c}/cope-{c}/zstat1.nii.gz')
    out_put_dir = os.path.join(third_level_dir, f'cope-{c}')

    if not os.path.exists(out_put_dir):
        os.makedirs(out_put_dir)

    # Smoothness estimation
    smooth = SmoothEstimate()
    smooth.inputs.zstat_file = zstat_file
    smooth.inputs.mask_file = mask_file
    smooth_est = smooth.run()

    # Ensure smooth_est outputs are valid
    dlh = smooth_est.outputs.dlh if smooth_est.outputs.dlh else 1.0  # Default value to avoid errors
    volume = smooth_est.outputs.volume if smooth_est.outputs.volume else 1.0

    # Cluster thresholding parameters
    threshold_pos = 2.3
    threshold_neg = -2.3  # Not used directly, but for reference
    connectivity = 26
    pthreshold = 0.05

    # **Positive threshold**
    cluster(
        input_file=zstat_file,
        threshold=threshold_pos,
        pthreshold=pthreshold,
        dlh=dlh,
        connectivity=connectivity,
        volume=volume,
        out_index_file=os.path.join(out_put_dir, 'cluster_index_pos.nii.gz'),
        out_threshold_file=os.path.join(out_put_dir, 'cluster_threshold_pos.nii.gz'),
        out_localmax_txt_file=os.path.join(out_put_dir, 'local_max_pos.txt')
    )

    # **Negative threshold workaround**
    neg_zstat_file = os.path.join(out_put_dir, "zstat1_neg.nii.gz")
    invert_command = f"/Users/xiaoqianxiao/fsl/bin/fslmaths {zstat_file} -mul -1 {neg_zstat_file}"
    run_command(invert_command)

    cluster(
        input_file=neg_zstat_file,
        threshold=threshold_pos,  # Using positive threshold on inverted image
        pthreshold=pthreshold,
        dlh=dlh,
        connectivity=connectivity,
        volume=volume,
        out_index_file=os.path.join(out_put_dir, 'cluster_index_neg.nii.gz'),
        out_threshold_file=os.path.join(out_put_dir, 'cluster_threshold_neg.nii.gz'),
        out_localmax_txt_file=os.path.join(out_put_dir, 'local_max_neg.txt')
    )

# #clustering
# mask_file = tpl_get(entities['space'],
#                             resolution=2,
#                             desc='brain',
#                             suffix='mask')  # Create a Cluster interface object
# contrast_dic = {'1':'Self_Case',
#              '2':'Other_Case',
#              '3':'Self_Other',
#              '4':'Self_Fixation',
#              '5':'Other_Fixation'
#              }
# contrast_list = list(contrast_dic.keys())
# from nipype.interfaces.fsl import SmoothEstimate
# for TR in ['1500', '1000']:
#     third_level_dir = (f'/Users/xiaoqianxiao/Experiment/RO1/selfother/derivatives/fMRI_analysis/thirdlevel_TR{TR}/stats')
#     for c in contrast_list:
#         zstat_file = os.path.join(third_level_dir, f'_contrast_{c}/stats/zstat1.nii.gz')
#         out_put_dir = os.path.join(third_level_dir, f'cope-{c}')
#         if not os.path.exists(out_put_dir):
#             os.makedirs(out_put_dir)
#         # First, estimate smoothness using fsl.SmoothEstimate
#         smooth = SmoothEstimate()
#         smooth.inputs.zstat_file = zstat_file  # Input z-stat image
#         smooth.inputs.mask_file = mask_file  # Input brain mask
#         # Run the smoothness estimation
#         smooth_est = smooth.run()
#
#         import subprocess
#         import os
#
#         def cluster(input_file, threshold, pthreshold, dlh, connectivity, volume, out_index_file, out_threshold_file,
#                     out_localmax_txt_file):
#             command = f"/Users/xiaoqianxiao/fsl/bin/fsl-cluster -i {input_file} -t {threshold} -p {pthreshold} -d {dlh} --connectivity={connectivity} --volume={volume} --oindex={out_index_file} --othresh={out_threshold_file} --olmax={out_localmax_txt_file}"
#             subprocess.run(command, shell=True, check=True)
#
#         #threshold = 3.2
#         threshold = 2.3
#         connectivity = 26
#         pthreshold = 0.05
#         dlh = smooth_est.outputs.dlh
#         volume = smooth_est.outputs.volume
#
#         out_index_file = os.path.join(out_put_dir, 'cluster_index.nii.gz')
#         out_threshold_file = os.path.join(out_put_dir, 'cluster_threshold.nii.gz')
#         out_localmax_txt_file = os.path.join(out_put_dir, 'local_max.txt')
#         input_file = zstat_file
#         cluster(input_file, threshold, pthreshold, dlh, connectivity, volume, out_index_file, out_threshold_file,
#                 out_localmax_txt_file)

#%%
#plots
#%%
import nibabel
from nilearn import plotting
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Or 'Qt5Agg', depending on your system

bgimage = nibabel.load(tpl_get(entities['space'],
                            resolution=2,
                            desc='brain',
                            suffix='T1w'))
#%%
results_dir = '/Users/xiaoqianxiao/Experiment/RO1/selfother/derivatives/fMRI_analysis/thirdlevel_TR1500/stats'
thresh_cluster_FE= nibabel.load(os.path.join(results_dir,'cope-3/cluster_threshold.nii.gz'))
#bgimage = nibabel.load(os.path.join(os.getenv('FSLDIR'),'data/standard/MNI152_T1_2mm_brain.nii.gz'))
map_display = plotting.plot_stat_map(thresh_cluster_FE,bgimage,threshold=3.2,title='Self VS. Others(TR1.5)')
plt.show()
#%%
results_dir = '/Users/xiaoqianxiao/Experiment/RO1/selfother/derivatives/fMRI_analysis/thirdlevel_TR1000/stats'
thresh_cluster_FE= nibabel.load(os.path.join(results_dir,'cope-3/cluster_threshold.nii.gz'))
#bgimage = nibabel.load(os.path.join(os.getenv('FSLDIR'),'data/standard/MNI152_T1_2mm_brain.nii.gz'))
map_display = plotting.plot_stat_map(thresh_cluster_FE,bgimage,threshold=3.2,title='Self VS. Others(TR1)')
plt.show()

#%%
results_dir = '/Users/xiaoqianxiao/Experiment/RO1/selfother/derivatives/fMRI_analysis/thirdlevel_TR1500/stats'
thresh_cluster_FE= nibabel.load(os.path.join(results_dir,'cope-2/cluster_threshold.nii.gz'))
#bgimage = nibabel.load(os.path.join(os.getenv('FSLDIR'),'data/standard/MNI152_T1_2mm_brain.nii.gz'))
map_display = plotting.plot_stat_map(thresh_cluster_FE,bgimage,threshold=3.2,title='Other VS. Case')
plt.show()

#%%
results_dir = '/Users/xiaoqianxiao/Experiment/RO1/selfother/derivatives/fMRI_analysis/thirdlevel_TR1500/stats'
thresh_cluster_FE= nibabel.load(os.path.join(results_dir,'cope-1/cluster_threshold.nii.gz'))
#bgimage = nibabel.load(os.path.join(os.getenv('FSLDIR'),'data/standard/MNI152_T1_2mm_brain.nii.gz'))
map_display = plotting.plot_stat_map(thresh_cluster_FE,bgimage,threshold=3.2,title='Self VS. Case')
plt.show()

#%%
results_dir = '/Users/xiaoqianxiao/Experiment/RO1/selfother/derivatives/fMRI_analysis/thirdlevel_TR1500/stats'
thresh_cluster_FE= nibabel.load(os.path.join(results_dir,'cope-4/cluster_threshold.nii.gz'))
#bgimage = nibabel.load(os.path.join(os.getenv('FSLDIR'),'data/standard/MNI152_T1_2mm_brain.nii.gz'))
map_display = plotting.plot_stat_map(thresh_cluster_FE,bgimage,threshold=3.2,title='Self VS. Fixation(TR1.5)')
plt.show()
#%%
results_dir = '/Users/xiaoqianxiao/Experiment/RO1/selfother/derivatives/fMRI_analysis/thirdlevel_TR1000/stats'
thresh_cluster_FE= nibabel.load(os.path.join(results_dir,'cope-4/cluster_threshold.nii.gz'))
#bgimage = nibabel.load(os.path.join(os.getenv('FSLDIR'),'data/standard/MNI152_T1_2mm_brain.nii.gz'))
map_display = plotting.plot_stat_map(thresh_cluster_FE,bgimage,threshold=3.2,title='Self VS. Fixation(TR1)')
plt.show()


#%%
#read error message
from nipype.utils.filemanip import loadcrash
data_dir = '/Users/xiaoqianxiao/PycharmProjects/SelfOther_MRI_dataAnalysis'
file_name = 'crash-20250210-075124-xiaoqianxiao-runinfo.a0-b939d8eb-66ab-4a7f-816b-70843a6b9799.pklz'
file_path = os.path.join(str(data_dir), file_name)
crash_data = loadcrash(file_path)
print(f"Node: {crash_data['node']}")
print(f"Traceback: {''.join(crash_data['traceback'])}")
#print(f"Error Message: {crash_data['node'].result.runtime.stderr}")


#%%
#rename
data_dir = '/Users/xiaoqianxiao/Experiment/RO1/selfother/derivatives/fmriprep/sub-004'

layout = BIDSLayout(str(data_dir), validate=False)
sub2_files = layout.get(session='pilotTR1000',
                        return_type='file')
import re
import shutil
for f in sub2_files:
    print(f)
    pattern = r'ses-pilotTR1000'
    print(pattern)
    bids_ref = re.sub(pattern, 'ses-Baseline', f)
    print(bids_ref)
    shutil.move(f, bids_ref)