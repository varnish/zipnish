import sys

def GenerateTraceURLId(idLong):
    return hex(idLong)

def ParseTraceURLId(hexString):
    return long(hexString, 16)

def findChildSpans(parent_id, dictionary):
    span_ids = []

    for key in dictionary:
        if key != parent_id and dictionary[key] == parent_id:
            span_ids.append(key)

    return span_ids


def findSpanDepth(current_depth, selected_span_id, parent_ids, dictionary):
    if selected_span_id in parent_ids:
        # find all the spans to which current_span is a parent and find the depth of each of them
        # selected the highest possible span depth
        #return findSpanDepth(current_depth + 1, selected_span_id, parent_ids, dictionary)
        childSpans = findChildSpans(selected_span_id, dictionary)

        if len(childSpans) == 0:
            return current_depth

        maxDepth = current_depth
        for child_span_id in childSpans:
            maxDepth = max(maxDepth, findSpanDepth(current_depth + 1, child_span_id, parent_ids, dictionary))

        return maxDepth

    return current_depth

def findTraceDepth(dictionary):
    parent_ids = []
    span_ids = []

    root_span_id = None

    for key in dictionary:
        if dictionary[key] is None:
            root_span_id = key

        if dictionary[key] is not None and dictionary[key] not in parent_ids:
            parent_ids.append(dictionary[key])

    # return 0 depth if we cannot find the root span
    if root_span_id is None:
        return 0

    return findSpanDepth(1, root_span_id, parent_ids, dictionary)

def generateTraceTimeMarkers(duration):
    timeSeq = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    timeMarkers = []

    for index in range(len(timeSeq)):
        timeMarkers.append({
                'index': index,
                'time': timeSeq[index] * duration
            })

    return timeMarkers

