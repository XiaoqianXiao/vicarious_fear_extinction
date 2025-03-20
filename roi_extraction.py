#%%
import os
import ssl
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets, image, plotting
from nilearn.image import resample_to_img
from templateflow.api import get as tpl_get
from nilearn.input_data import NiftiSpheresMasker

output_dir = "/Users/xiaoqianxiao/tool/parcellation/ROIs"
os.makedirs(output_dir, exist_ok=True)

your_data_path = tpl_get('MNI152NLin2009cAsym', resolution=2, desc='brain', suffix='mask')
your_img = nib.load(your_data_path)

roi_files = {}

#use the unthresholded Harvard-Oxford subcortical atlas (thr0)
ho_atlas = datasets.fetch_atlas_harvard_oxford("sub-maxprob-thr0-1mm")
ho_img = image.load_img(ho_atlas.maps)
#%%
cho_atlas = datasets.fetch_atlas_harvard_oxford("cort-maxprob-thr0-1mm")
cho_img = image.load_img(cho_atlas.maps)
#%%
# Schaefer atlas for vmPFC (using the 400-parcel version)
schaefer_atlas = datasets.fetch_atlas_schaefer_2018(n_rois=400, resolution_mm=2)
schaefer_img = image.load_img(schaefer_atlas.maps)
labels = schaefer_atlas.labels  # List of ROI names
lh_vmpfc_roi_indices = []
rh_vmpfc_roi_indices = []
for idx, label in enumerate(labels, start=1):  # ROI indices start at 1
    label_str = str(label).lower()
    # Criteria: Default Mode Network PFC regions (common for vmPFC)
    if 'default' in label_str and 'pfc' in label_str:
        if 'lh' in label_str:
            lh_vmpfc_roi_indices.append(idx)
            print(f"Left Hemisphere ROI {idx}: {label}")
        elif 'rh' in label_str:
            rh_vmpfc_roi_indices.append(idx)
            print(f"Right Hemisphere ROI {idx}: {label}")
#%%
lh_mask_formula = "np.isin(img, {})".format(lh_vmpfc_roi_indices)
lh_vmpfc_mask = image.math_img(lh_mask_formula, img=schaefer_img)
roi_mask_path = os.path.join(output_dir, f"lh_vmpfc_mask.nii.gz")
lh_vmpfc_mask.to_filename(roi_mask_path)
roi_files['lh_vmpfc'] = roi_mask_path
rh_mask_formula = "np.isin(img, {})".format(rh_vmpfc_roi_indices)
rh_vmpfc_mask = image.math_img(rh_mask_formula, img=schaefer_img)
roi_mask_path = os.path.join(output_dir, f"rh_vmpfc_mask.nii.gz")
rh_vmpfc_mask.to_filename(roi_mask_path)
roi_files['rh_vmpfc'] = roi_mask_path



#%%
atlas_shape = cho_img.shape
midpoint = atlas_shape[0] // 2
roi_indices_CHO = {
    "insula":2,
    "ACC": 29
}
for roi, index in roi_indices_CHO.items():
    roi_mask = image.math_img(f"(img == {index}) * (np.arange(img.shape[0])[:, None, None] < {midpoint})", img=cho_img)
    roi_mask_path = os.path.join(output_dir, f"lh_{roi}_mask.nii.gz")
    roi_mask.to_filename(roi_mask_path)
    roi_files[f'lh{roi}'] = roi_mask_path
    roi_mask = image.math_img(f"(img == {index}) * (np.arange(img.shape[0])[:, None, None] > {midpoint})", img=cho_img)
    roi_mask_path = os.path.join(output_dir, f"rh_{roi}_mask.nii.gz")
    roi_mask.to_filename(roi_mask_path)
    roi_files[f'rh{roi}'] = roi_mask_path

#%%
# Harvard-Oxford atlas indices as provided:
roi_indices_HO = {
    "lh_amygdala": 10,    # Left Amygdala
    "rh_amygdala": 20,   # Right Amygdala
    "lh_hippocampus": 9,    # Left Hippocampus
    "rh_hippocampus": 19   # Right Hippocampus
}
for roi, index in roi_indices_HO.items():
    roi_mask = image.math_img(f"(img == {index})", img=ho_img)
    roi_mask_path = os.path.join(output_dir, f"{roi}_mask.nii.gz")
    roi_mask.to_filename(roi_mask_path)
    roi_files[roi] = roi_mask_path

print("All ROI masks saved in:", output_dir)
print("Mask files:", roi_files)

#%%
def needs_resampling(source_img, target_img):
    return not np.allclose(source_img.affine, target_img.affine) or \
           source_img.header.get_zooms() != target_img.header.get_zooms()

#%%
roi_dir="/Users/xiaoqianxiao/tool/parcellation/ROIs"
ref="/Users/xiaoqianxiao/.cache/templateflow/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-02_desc-brain_mask.nii.gz"
for mask in $roi_dir/*.nii.gz; do
    base=$(basename "$mask" .nii.gz)
    flirt -in "$mask" -ref "$ref" -out "${roi_dir}/resampled/${base}.nii.gz" \
      -applyxfm -usesqform -interp nearestneighbour
done

#%%
import os
import nibabel as nib
import numpy as np
import pandas as pd

def extract_cope_from_rois(cope_file, roi_dir, task, contrast, extracted_data):
    """
    Extract mean COPE values from a 4D merged COPE file using ROI masks and append results to a list.

    Parameters:
        cope_file (str): Path to the merged_cope.nii.gz file (4D: X, Y, Z, subjects).
        roi_dir (str): Path to the directory containing ROI masks (.nii.gz files).
        task (str): Task name.
        contrast (int): Contrast number.
        extracted_data (list): List to store extracted results.
    """
    # Load the 4D COPE file (X, Y, Z, N_subjects)
    cope_img = nib.load(cope_file)
    cope_data = cope_img.get_fdata()
    num_subjects = cope_data.shape[-1]

    # Iterate over ROI files in the directory
    for roi_file in os.listdir(roi_dir):
        if roi_file.endswith('mask.nii.gz'):
            roi_path = os.path.join(roi_dir, roi_file)
            roi_img = nib.load(roi_path)
            roi_data = roi_img.get_fdata()

            # Ensure the ROI mask has the same spatial dimensions as the COPE file (excluding time dimension)
            if roi_data.shape != cope_data.shape[:-1]:  # Ignore last dimension (subjects)
                print(f"Skipping {roi_file}: Dimension mismatch")
                continue

            # Extract mean COPE value for each subject
            roi_name = os.path.splitext(os.path.splitext(roi_file)[0])[0]  # Remove .nii.gz extension
            for subj in range(num_subjects):
                subject_cope = cope_data[..., subj]  # Extract subject's 3D cope data
                masked_data = subject_cope[roi_data > 0]  # Apply ROI mask

                mean_cope_value = np.mean(masked_data) if masked_data.size > 0 else np.nan
                extracted_data.append({
                    "Subject": subj + 1,
                    "Task": task,
                    "Contrast": contrast,
                    "ROI": roi_name,
                    "Mean_COPE_Value": mean_cope_value
                })

# Define paths
root_dir = '/Users/xiaoqianxiao/projects'
project_name = 'NARSAD'
data_dir = os.path.join(root_dir, project_name, 'MRI')
derivatives_dir = os.path.join(data_dir, 'derivatives')
results_dir = os.path.join(derivatives_dir, 'fMRI_analysis/groupLevel')
roi_dir = "/Users/xiaoqianxiao/tool/parcellation/ROIs/resampled"
output_csv = os.path.join(results_dir, 'roi_cope_results_all.csv')  # Single output file

tasks = ['phase2', 'phase3']
contr_list = list(range(1, 26))

# List to store all extracted results
all_extracted_data = []

for task in tasks:
    task_results_dir = os.path.join(results_dir, f'task-{task}')
    for contrast in contr_list:
        cope_file = os.path.join(task_results_dir, f'cope{contrast}', 'merged_cope.nii.gz')
        if os.path.exists(cope_file):
            extract_cope_from_rois(cope_file, roi_dir, task, contrast, all_extracted_data)
        else:
            print(f"Skipping missing file: {cope_file}")

# Convert results to a DataFrame and save
df = pd.DataFrame(all_extracted_data)
df.to_csv(output_csv, index=False)
print(f"Results saved to {output_csv}")