import numpy as np
import ubelt as ub
import kwcoco


# For computing bbox overlap
def boxoverlap(bb, bbgt):
    bb = bb.copy()
    bbgt = bbgt.copy()
    # convert to [xmin, ymin, xmax, ymax]
    bb[2] += bb[0]
    bb[3] += bb[1]
    bbgt[2] += bbgt[0]
    bbgt[3] += bbgt[1]

    ov = 0
    iw = np.min((bb[2], bbgt[2])) - np.max((bb[0], bbgt[0])) + 1
    ih = np.min((bb[3], bbgt[3])) - np.max((bb[1], bbgt[1])) + 1
    if iw > 0 and ih > 0:
        # compute overlap as area of intersection / area of union
        intersect = iw * ih
        ua = (bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) + \
            (bbgt[2] - bbgt[0] + 1.) * \
            (bbgt[3] - bbgt[1] + 1.) - intersect
        ov = intersect / ua
    return ov


def main():
    dset = kwcoco.CocoDataset.demo('vidshapes16', num_frames=30)
    data = dset.dataset
    for img in dset.imgs.values():
        img['frame_id'] = img['frame_index']

    with ub.Timer('old method'):
        all_ious = []
        frame_to_ious2 = ub.ddict(list)

        for video in data['videos']:
            video_id = video['id']
            # get all corresponding frames in video
            image_list = [(d['id'], d['frame_id'])
                          for d in data['images'] if d['video_id'] == video_id]
            # get all corresponding bboxes for each frame in video
            bbox_dict = {image[1]: [(d['track_id'], d['bbox']) for d in data['annotations']
                                    if d['image_id'] == image[0]] for image in image_list}
            for frame, bbox_list in bbox_dict.items():
                frame_ious = []
                for trk_id, bbox in bbox_list:
                    if trk_id > -1:
                        ious = []
                        for i in range(-10, 11):
                            # get offset frame c
                            frame_c = frame + i
                            if 1 <= frame_c < len(image_list) and i != 0:
                                # get all bboxes in frame c with same track id
                                bbox_c = bbox_dict[frame_c]
                                for c_trk_id, c_bbox in bbox_c:
                                    if trk_id == c_trk_id:
                                        iou = boxoverlap(bbox, c_bbox)
                                        ious.append(iou)
                                        break

                        frame_ious.append(np.mean(ious))
                        frame_to_ious2[frame].append(np.mean(ious))
                if frame_ious:  # if this frame has no boxes we add a 0.0
                    all_ious.append(frame_ious)
                else:
                    all_ious.append([0.0])

    with ub.Timer('new method'):
        all_ious = []

        # Precompute groups for fast lookup
        trackid_to_anns = ub.group_items(data['annotations'], lambda x: x['track_id'])

        vidid_to_trackids = ub.ddict(list)
        for tid, anns in trackid_to_anns.items():
            ann = ub.peek(anns)
            gid = ann['image_id']
            img = dset.imgs[gid]
            vidid = img['video_id']
            vidid_to_trackids[vidid].append(tid)

        frame_to_ious = ub.ddict(list)
        frame_to_all_ious1 = ub.ddict(list)

        for video in data['videos']:
            video_id = video['id']

            trackids = vidid_to_trackids[video_id]
            video_tracks = ub.dict_subset(trackid_to_anns, trackids)

            for tid, anns in video_tracks.items():
                # track_ious = []

                # For this track, find each frame id and each box position
                frame_ids = []
                box_list = []
                for ann in anns:
                    gid = ann['image_id']
                    img = dset.imgs[gid]
                    fid = img['frame_id']
                    frame_ids.append(fid)
                    box_list.append(ann['bbox'])

                # Aggregate into a Boxes object for faster computation
                import kwimage
                frame_ids = np.array(frame_ids)
                boxes = kwimage.Boxes(np.array(box_list), 'xywh')

                # For each frame, compute the ious between neighbors
                time_threshold = 10
                for fidx, fid in enumerate(frame_ids):
                    # TODO: this is brute force and likely could be faster
                    # Determine which frames to compare against
                    mask = np.abs(frame_ids - fid) <= time_threshold
                    mask[fidx] = False  # dont compare against self

                    curr_box = boxes.take([fidx])
                    neighbor_boxes = boxes.compress(mask)

                    ious = curr_box.ious(neighbor_boxes, bias=1.0)
                    frame_to_all_ious1[fid].append(ious)
                    # track_ious.append(ious)
                    frame_to_ious[fid].append(ious.mean())

        all_ious = {fid: ious.mean() for fid, ious in frame_to_ious.items()}
