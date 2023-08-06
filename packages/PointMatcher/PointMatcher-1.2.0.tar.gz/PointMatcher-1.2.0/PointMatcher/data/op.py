import collections


def count_all_keypoints(matching):
    n = 0
    for view in matching.get_views():
        n += len(view['keypoints'])
    return n


def grouping(matching):
    ma = matching.data.copy()
    for v in ma['views']:
        v['picked'] = [False for _ in range(len(v['keypoints']))]

    current_idx = 0
    groups = {current_idx: []}

    def f(view_idx, keypoint_idx):
        if ma['views'][view_idx]['picked'][keypoint_idx]:
            return
        else:
            ma['views'][view_idx]['picked'][keypoint_idx] = True
            groups[current_idx].append((view_idx, keypoint_idx))
            view_id = ma['views'][view_idx]['id_view']
            for p in ma['pairs']:
                if p['id_view_i'] == view_id:
                    for m in p['matches']:
                        if m[0] == keypoint_idx:
                            view_idx_next = matching.find_view_idx(p['id_view_j'])
                            keypoint_idx_next = m[1]
                            f(view_idx_next, keypoint_idx_next)
                elif p['id_view_j'] == view_id:
                    for m in p['matches']:
                        if m[1] == keypoint_idx:
                            view_idx_next = matching.find_view_idx(p['id_view_i'])
                            keypoint_idx_next = m[0]
                            f(view_idx_next, keypoint_idx_next)

    for view_idx_ in range(len(ma['views'])):
        for keypoint_idx_ in range(len(ma['views'][view_idx_]['keypoints'])):
            if 0 < len(groups[current_idx]):
                current_idx += 1
                groups[current_idx] = []
            f(view_idx_, keypoint_idx_)

    # check
    count_all_1 = count_all_keypoints(matching)
    count_all_2 = 0
    for x in groups:
        count_all_2 += len(groups[x])
    assert count_all_1 == count_all_2

    return groups


def sanity_check(matching):
    groups = grouping(matching)
    bad_keypoints = []
    for key in groups:
        view_indices = [x[0] for x in groups[key]]
        bad_view_indices = [item for item, count in collections.Counter(view_indices).items() if count > 1]
        if 0 < len(bad_view_indices):
            for x in groups[key]:
                if x[0] in bad_view_indices:
                    bad_keypoints.append(x)
    return bad_keypoints
