"""
Stable recipes whose function signatures should almost never change in the future.
"""
from bokeh.layouts import row
from hover.utils.bokeh_helper import servable
from .subroutine import standard_annotator, standard_finder


@servable(title="Simple Annotator")
def simple_annotator(dataset, height=600, width=600):
    """
    The most basic recipe, which nonetheless can be useful with decent 2-d embedding.

    Layout:

    sidebar | [annotate here]
    """
    annotator = standard_annotator(dataset, height=height, width=width)

    sidebar = dataset.view()
    layout = row(sidebar, annotator.view())
    return layout


@servable(title="Linked Annotator")
def linked_annotator(dataset, height=600, width=600):
    """
    Leveraging CorpusFinder which has the best search highlights.

    Layout:

    sidebar | [search here] | [annotate here]
    """
    finder = standard_finder(dataset, height=height, width=width)
    annotator = standard_annotator(dataset, height=height, width=width)

    # link coordinates and selections
    finder.link_xy_range(annotator)
    finder.link_selection("raw", annotator, "raw")

    sidebar = dataset.view()
    layout = row(sidebar, finder.view(), annotator.view())
    return layout
