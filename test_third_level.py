import os
from nipype import config
import nibabel as nib
from bids.layout import BIDSLayout
from templateflow.api import get as tpl_get
import pandas as pd

# Set FSL environment
os.environ['FSLDIR'] = '/Users/xiaoqianxiao/fsl'
os.environ['PATH'] = f"/Users/xiaoqianxiao/fsl/share/fsl/bin:/Users/xiaoqianxiao/fsl/bin:{os.environ['PATH']}"
print("PATH:", os.environ['PATH'])
print("Cluster location:", os.popen('which cluster').read().strip())

from third_level import third_level_wf

# Define directories
root_dir = '/Users/xiaoqianxiao/projects'
project_name = 'NARSAD'
data_dir = os.path.join(root_dir, project_name, 'MRI')
derivatives_dir = os.path.join(data_dir, 'derivatives')
work_dir = os.path.join(derivatives_dir, 'work_flows')
output_dir = os.path.join(derivatives_dir, 'fMRI_analysis')
for d in [work_dir, output_dir]:
    os.makedirs(d, exist_ok=True)
sub_no_MRI = ['N102', 'N208']
project_dir = '/Users/xiaoqianxiao/projects/NARSAD'
SCR_dir = os.path.join(project_dir, 'EDR')
drug_file = os.path.join(SCR_dir, 'drug_order.csv')
ECR_file = os.path.join(SCR_dir, 'ECR.csv')

# Load behavioral data
df_drug = pd.read_csv(drug_file)
df_drug['group'] = df_drug['subID'].apply(lambda x: 'Patients' if x.startswith('N1') else 'Controls')
df_ECR = pd.read_csv(ECR_file)
df_behav = df_drug.merge(df_ECR, how='left', left_on='subID', right_on='subID')
group_info = list(df_behav.loc[~df_behav['subID'].isin(sub_no_MRI), ['subID', 'group', 'Drug']].itertuples(index=False, name=None))

# Align sub_list with group_info
sub_list = ['N101', 'N103', 'N201', 'N202']
group_info = [info for info in group_info if info[0] in sub_list]

# Load first-level data
firstlevel_dir = os.path.join(derivatives_dir, 'fMRI_analysis/firstlevel')
glayout = BIDSLayout(firstlevel_dir, validate=False, config=['bids', 'derivatives'])
contr_list = [1, 2, 3, 4, 5, 6]
tasks = ['phase2']

# Collect COPE and VARCOPE files per contrast
def collect_task_data(task, contrast):
    copes, varcopes = [], []
    for sub in sub_list:
        cope_file = glayout.get(subject=sub, task=task, desc=f'cope{contrast}',
                                extension=['.nii', '.nii.gz'], return_type='file')
        varcope_file = glayout.get(subject=sub, task=task, desc=f'varcope{contrast}',
                                   extension=['.nii', '.nii.gz'], return_type='file')
        if cope_file and varcope_file:
            copes.append(cope_file[0])
            varcopes.append(varcope_file[0])
        else:
            print(f"Missing files for task-{task}, sub-{sub}, cope{contrast}")
    return copes, varcopes

# Enable debug mode
config.enable_debug_mode()

# Process each task
for task in tasks:
    print(f"\nProcessing task: {task}")
    task_work_dir = os.path.join(work_dir, f'task-{task}')
    task_output_dir = os.path.join(output_dir, f'task-{task}')
    design_dir = os.path.join(task_output_dir, 'design_files')
    os.makedirs(task_work_dir, exist_ok=True)
    os.makedirs(design_dir, exist_ok=True)

    # Initialize workflow with 3mm mask
    group_mask = str(tpl_get(glayout.get(task=task)[0].entities['space'], resolution=3, desc='brain', suffix='mask'))
    wf = third_level_wf(output_dir=task_output_dir, bids_ref=None, c=1, name=f"third_level_{task}")
    wf.inputs.inputnode.group_mask = group_mask
    wf.inputs.inputnode.group_info = group_info
    wf.base_dir = task_work_dir

    # Process each contrast
    for contrast in contr_list:
        print(f"Processing contrast: {contrast}")
        copes, varcopes = collect_task_data(task, contrast)
        if len(copes) != 4 or len(varcopes) != 4:
            print(f"Skipping contrast {contrast}: Expected 4 subjects, got copes={len(copes)}, varcopes={len(varcopes)}")
            continue

        wf.inputs.inputnode.in_copes = copes
        wf.inputs.inputnode.in_varcopes = varcopes
        print(f"Task-{task} Contrast-{contrast} Inputs: mask={group_mask}, copes={len(copes)}, varcopes={len(varcopes)}, group_info={group_info}")

        # Run the workflow
        result = wf.run(plugin="Linear")

        # Verify outputs
        outputnode = wf.get_node('outputnode')
        outputs = outputnode.result.outputs if outputnode.result else None
        print(f"Task-{task} Contrast-{contrast} Outputs:", outputs)
        if outputs:
            for field in ["zstats_raw", "zstats_clust", "clust_index_file", "clust_localmax_txt_file", "zstats_fwe"]:
                output = getattr(outputs, field, None)
                print(f"{field}: {output}")
                if output and (isinstance(output, str) and not os.path.exists(output)) or (isinstance(output, list) and not all(os.path.exists(f) for f in output)):
                    print(f"Warning: {field} files missing")
            zstats_img = nib.load(outputs.zstats_raw)
            assert zstats_img.shape[-1] == 3, f"Expected 3 contrasts, got {zstats_img.shape[-1]}"
            print(f"Task-{task} Contrast-{contrast}: All outputs generated successfully!")
        else:
            print(f"Task-{task} Contrast-{contrast}: No outputs collected.")