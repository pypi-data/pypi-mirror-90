from AnnotatedTree.ParseTreeDrawable cimport ParseTreeDrawable


cdef class TreeAutoSemantic:

    cpdef autoLabelSingleSemantics(self, ParseTreeDrawable parseTree):
        pass

    cpdef autoSemantic(self, ParseTreeDrawable parseTree):
        if self.autoLabelSingleSemantics(parseTree):
            parseTree.saveWithFileName()
