

def main(*args):
    print "-" *30
    print args
    print "-" *30
    return {
        "extra_assets": [
            "/path1",
            "/path2"
        ]
    }


########## KEEP FOR NOW WHILE WE FIGURE OUT HOW TO EXPORT ASS
#  commands = [
#     # Render Setup window must be closed, otherwise setting rendTimeType and
#     # rendPickupFrames might not stick, according to Autodesk
#     # https://help.autodesk.com/view/3DSMAX/2017/ENU/?guid=__files_GUID_30AF1E53_5A69_402D_84D6_4D6ECCDD6D20_htm
#     'renderSceneDialog.close()',
#     # rendTimeType 4 is equivalent to "Frames" in
#     # "Render Setup -> Common -> TimeOutput" and it expects the frame range
#     # to be specified via rendPickupFrames
#     'rendTimeType=4',
#     'rendPickupFrames="%s-%s"' % (start_frame, end_frame),
#     'rendNThFrame=1',
#     'renderers.current.export_to_ass = true',
#     'renderers.current.ass_file_path = "%s"' % file_name,
#     'render fromFrame:%s toFrame:%s vfb:false' % (start_frame, end_frame)
# ]

# command = ';'.join(commands)
# maybe_error = MaxPlus.FPValue()
# if not MaxPlus.Core.EvalMAXScript(command, maybe_error):
#     raise RuntimeError(str(maybe_error))

# import MaxPlus

# # MaxPlus.Core.EvalMAXScript(command, maybe_error):
    
    
# import pymxs
# rt = pymxs.runtime

# print "initialized"
# print rt.renderers
# print dir(rt.renderers)
# print rt.renderers.current
# print dir(rt.renderers.current)
# print rt.renderers.current.ass_file_path
# rt.renderers.current.ass_file_path = "W:/perishable/max_proj/foo"
# print rt.renderers.current.export_to_ass
# rt.renderSceneDialog.close()

# rt.renderers.current = rt.Arnold

# rt.renderers.current = rt.RendererClass.classes[0]()
# print rt.renderers.current

# print dir(rt.RendererClass.classes[0]())

# print rt.RendererClass.classes
# for klass in rt.RendererClass.classes:
#     print dir(klass)
    
    
# print rt.Arnold