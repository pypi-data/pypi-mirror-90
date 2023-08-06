from AnnotatedSentence.ViewLayerType import ViewLayerType


cdef class IsNullElement(IsLeafNode):

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        cdef str data, parentData
        if super().satisfies(parseNode):
            data = parseNode.getLayerData(ViewLayerType.ENGLISH_WORD)
            parentData = parseNode.getParent().getData().getName()
            return "*" in data or (data == "0" and parentData == "-NONE-")
        return False
