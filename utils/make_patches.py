import numpy as np
import cv2
import h5py
import extract_dcts 

def im_to_bytes(patch):
    # NEW CV2 CODE
    _, im_buf_arr = cv2.imencode(".jpeg", patch, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return im_buf_arr.tobytes()

def make_patches(im, size, to_bytes=True):
    patches = []
    for i in range(0, im.shape[0]-size+1, size):
        for j in range(0, im.shape[1]-size+1, size):
            # append byte form of images
            image = im[i:i+size, j:j+size]
            if to_bytes:
                image = im_to_bytes(image)
            patches.append(image)
    return patches

def resize(image, downscale_factor):
    return cv2.resize(image, image.shape[0] / downscale_factor, image.shape[0] / downscale_factor) if downscale_factor > 1 else image


def builder(input, task, examples, labels):
    his_size = input.his_size
    # initialise dataset 
    with h5py.File(f'processed/DCT_{task}_{input.dset_name}.h5', 'w') as f:
        _ = f.create_dataset('DCT', shape=(0, his_size), maxshape=(None, his_size))
        _ = f.create_dataset('labels', shape=(0, 2), maxshape=(None, 2))
    
    
        # generate patches from an image and extract the dcts from each patch and store in dataset
        for im_num, (path, label) in enumerate(zip(examples, labels)):
            # with h5py.File(f'processed/DCT_{task}_{input.dset_name}.h5', 'a') as Dset:

                image = cv2.cvtColor(cv2.imread(path), input.colour_space)
                image = resize(image, input.downscale_factor)
            
                if input.patch_size:
                    patches = make_patches(image, input.patch_size)

                # extract dct histograms from each patch 
                patch_histograms = extract_dcts.process(patches, input)


                #iterate over all patches
                for patch_histogram in patch_histograms:

                    dct_dset = f['DCT']
                    dct_dset.resize((dct_dset.shape[0] + 1, his_size))
                    dct_dset[-1] = patch_histogram
                    
                    labels_dset = f['labels']
                    labels_dset.resize((labels_dset.shape[0] + 1, 2))
                    labels_dset[-1] = np.array([label, im_num])



 