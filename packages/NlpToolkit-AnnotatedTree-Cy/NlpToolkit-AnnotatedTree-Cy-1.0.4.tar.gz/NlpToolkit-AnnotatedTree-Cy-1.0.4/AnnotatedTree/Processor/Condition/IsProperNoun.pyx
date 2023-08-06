from AnnotatedTree.ParseNodeDrawable cimport ParseNodeDrawable
from AnnotatedTree.Processor.Condition.IsLeafNode cimport IsLeafNode


cdef class IsProperNoun(IsLeafNode):

    cpdef bint satisfies(self, ParseNodeDrawable parseNode):
        cdef str parentData
        if super().satisfies(parseNode):
            parentData = parseNode.getParent().getData().getName()
            return parentData == "NNP" or parentData == "NNPS"
        return False
