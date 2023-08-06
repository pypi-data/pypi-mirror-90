"""
@file
@brief Shorten code in notebook :ref:`onnxsklearnconsortiumrst`.
"""
import os
import sys
from collections import OrderedDict
import warnings
from pyquickhelper.pycode.profiling import profile
from pyquickhelper.helpgen.rst_converters import docstring2html
from pyensae.graphhelper import draw_diagram
from jyquickhelper import RenderJsDot
import sklearn
from skl2onnx.proto import TensorProto
from onnx import helper


def graph_persistence_pickle():
    """
    See :ref:`onnxsklearnconsortiumrst`.
    """
    return draw_diagram("""
        blockdiag {
            default_fontsize = 20; node_width = 200; node_height = 100;
            model[label="trained model\\nscikit-learn"];
            pkl[label="pickled model"];
            rest[label="restored model\\nscikit-learn", textcolor="#00AAAA"];
            pkl -> rest;
            pred[label="predictions"];
            train[label="training"];
            group {
                label = "machine 1";
                color = "#FFAAAA";
                model -> pkl; pkl;
            }
            group {
                label = "machine 2";
                color = "#AAFFAA";
                rest -> pred; rest -> train;
            }
        }""")


def graph_persistence_pickle_issues():
    """
    See :ref:`onnxsklearnconsortiumrst`.
    """
    return draw_diagram("""
        blockdiag {
            default_fontsize = 20; node_width = 200; node_height = 100;
            pkl[label="pickled model"];
            rest[label="restored model\\nscikit-learn\\nUNSTABLE", textcolor="#00AAAA"];
            pkl -> rest;
            pred[label="predictions\\nSLOW"];
            train[label="training"];
            group {
                label = "machine 1";
                color = "#FFAAAA"; pkl;
            }
            group {
                label = "machine 2";
                color = "#AAFFAA";
                rest -> pred; rest -> train;
            }
        }""")


def graph_persistence_onnx():
    """
    See :ref:`onnxsklearnconsortiumrst`.
    """
    return draw_diagram("""
        blockdiag {
            default_fontsize = 20; node_width = 200; node_height = 100;
            model[label="trained model\\nscikit-learn"];
            onnx[label="ONNX model"];
            rest[label="ONNX runtime", textcolor="#00AAAA"];
            onnx -> rest;
            pred[label="predictions"];
            notrain[label="cannot train", color="#FF0000"];
            group {
                label = "machine 1";
                color = "#FFAAAA";
                model -> onnx[label="conversion"];
                onnx;
            }
            group {
                label = "machine 2";
                color = "#AAFFAA";
                rest ;
                pred;
                rest -> pred;
                rest -> notrain[folded];
            }
        }""")


def graph_three_components():
    """
    See :ref:`onnxsklearnconsortiumrst`.
    """
    return draw_diagram("""
        blockdiag {
            default_fontsize = 20; node_width = 200; node_height = 100;
            onnx[label="ONNX\\n\\nset of mathematical functions", color="#FFFF00"];
            conv[label="converter\\n\\nsklearn-onnx", color="#FFFF00"];
            run[label="runtime\\n\\nonnxruntime\\nonnx.js\\n...", color="#FFFF00"];
            onnx -> conv -> run ;
        }""")


def profile_fct_graph(fct, title, highlights=None, nb=20, figsize=(10, 3)):
    """
    Returns a graph which profiles the execution of function *fct*.
    See :ref:`onnxsklearnconsortiumrst`.
    """
    paths = [os.path.dirname(sklearn.__file__),
             "site-packages",
             os.path.join(sys.prefix, "lib")]
    _, df = profile(fct, as_df=True, rootrem=paths)
    colname = 'namefct' if 'namefct' in df.columns else 'fct'
    sdf = df[[colname, 'cum_tall']].head(n=nb).set_index(colname)
    index_list = list(sdf.index)
    ax = sdf.plot(kind='bar', figsize=figsize, rot=30)
    ax.set_title(title)
    for la in ax.get_xticklabels():
        la.set_horizontalalignment('right')
    if highlights:
        for lab in highlights:
            if lab not in index_list:
                new_labs = [ns for ns in index_list if isinstance(
                    ns, str) and lab in ns]
                if len(new_labs) == 0:
                    raise ValueError("Unable to find '{}' in '{}'?".format(
                        lab, ", ".join(sorted(map(str, index_list)))))
                labs = new_labs
            else:
                labs = [lab]
            for la in labs:
                pos = sdf.index.get_loc(la)
                h = 0.15
                ax.plot([pos - 0.35, pos - 0.35], [0, h], 'r--')
                ax.plot([pos + 0.3, pos + 0.3], [0, h], 'r--')
                ax.plot([pos - 0.35, pos + 0.3], [h, h], 'r--')
    return ax


def onnx2str(model_onnx, nrows=15):
    """
    Displays the beginning of an ONNX graph.
    See :ref:`onnxsklearnconsortiumrst`.
    """
    lines = str(model_onnx).split('\n')
    if len(lines) > nrows:
        lines = lines[:nrows] + ['...']
    return "\n".join(lines)


def onnx2dotnb(model_onnx, width="100%", orientation="LR"):
    """
    Converts an ONNX graph into dot then into :epkg:`RenderJsDot`.
    See :ref:`onnxsklearnconsortiumrst`.
    """
    from onnx.tools.net_drawer import GetPydotGraph, GetOpNodeProducer
    pydot_graph = GetPydotGraph(
        model_onnx.graph, name=model_onnx.graph.name, rankdir=orientation,
        node_producer=GetOpNodeProducer("docstring", color="yellow",
                                        fillcolor="yellow", style="filled"))
    dot = pydot_graph.to_string()
    return RenderJsDot(dot, width=width)


def onnx2graph(onnx_model):
    """
    Converts an :epkg:`ONNX` model into a readable graph.

    @param      onnx_model      onnx_model
    @return                     graph defined with :epkg:`OrderedDict`
                                so that it can be processed by epkg:`asciitree`
    """
    vars = {}

    for node in onnx_model.graph.node:
        key = "%s[%s]" % (node.name, node.op_type)
        for inp in node.input:
            if inp not in vars:
                vars[inp] = []
            if key not in vars[inp]:
                vars[inp].append(key)
        vars[key] = []
        for out in node.output:
            if out not in vars[key]:
                vars[key].append(out)

    return edges2asciitree(vars)


def edges2asciitree(edges):
    """
    Converts a set of edges into a combination
    of :epkg:`OrderedDict` which can be understood
    by :epkg:`asciitree`. This does not work if one node
    has multiple inputs.

    @param      edges       set of edges
    @return                 :epkg:`OrderedDict`

    .. runpython::
        :showcode:

        data = {'X': ['LinearClassifier[LinearClassifier]'],
                'LinearClassifier[LinearClassifier]':
                    ['label', 'probability_tensor'],
                'probability_tensor': ['Normalizer[Normalizer]'],
                'Normalizer[Normalizer]': ['probabilities'],
                'label': ['Cast[Cast]'],
                'Cast[Cast]': ['output_label'],
                'probabilities': ['ZipMap[ZipMap]'],
                'ZipMap[ZipMap]': ['output_probability']}

        from jupytalk.talk_examples.sklearn2019 import edges2asciitree
        res = edges2asciitree(data)

        import pprint
        pprint.pprint(res)

        from asciitree import LeftAligned
        tr = LeftAligned()
        print(tr(res))
    """
    roots = []
    values = []
    for _, eds in edges.items():
        values.extend(eds)
    vs = set(values)
    for key in edges:
        if key not in vs:
            roots.append(key)

    if len(roots) > 1:
        edges = edges.copy()
        edges['root'] = roots
        roots = ['root']

    res = OrderedDict()
    find = {}
    for r in roots:
        res[r] = OrderedDict()
        find[r] = res[r]

    modif = 1
    while modif > 0:
        modif = 0
        for k, eds in edges.items():
            if k in find:
                ord = find[k]
                for edge in eds:
                    if edge not in ord:
                        ord[edge] = OrderedDict()
                        find[edge] = ord[edge]
                        modif += 1

    return res


def onnxdocstring2html(doc, start="number of targets."):
    """
    Converts the ONNX documentation into rst.
    """
    if start is not None:
        doc = doc.split(start)[-1]
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        return docstring2html(doc.replace("Default value is ````", ""))


def rename_input_output(model_onnx):
    """
    Renames all input and output of an ONNX file.
    """
    def clean_name(name):
        return name.replace("_", "")

    def copy_inout(inout):
        shape = [s.dim_value for s in inout.type.tensor_type.shape.dim]
        value_info = helper.make_tensor_value_info(
            clean_name(inout.name),
            inout.type.tensor_type.elem_type,
            shape)
        return value_info

    graph = model_onnx.graph
    inputs = [copy_inout(o) for o in graph.input]
    outputs = [copy_inout(o) for o in graph.output]
    nodes = []
    for node in graph.node:
        n = helper.make_node(node.op_type,
                             [clean_name(o) for o in node.input],
                             [clean_name(o) for o in node.output])
        n.attribute.extend(node.attribute)  # pylint: disable=E1101
        nodes.append(n)

    inits = []
    for o in graph.initializer:
        tensor = TensorProto()
        tensor.data_type = o.data_type
        tensor.name = clean_name(o.name)
        tensor.raw_data = o.raw_data
        tensor.dims.extend(o.dims)  # pylint: disable=E1101
        inits.append(tensor)

    graph = helper.make_graph(nodes, graph.name, inputs, outputs, inits)
    onnx_model = helper.make_model(graph)
    onnx_model.ir_version = model_onnx.ir_version
    onnx_model.producer_name = model_onnx.producer_name
    onnx_model.producer_version = model_onnx.producer_version
    onnx_model.domain = model_onnx.domain
    onnx_model.model_version = model_onnx.model_version
    onnx_model.doc_string = model_onnx.doc_string
    return onnx_model
