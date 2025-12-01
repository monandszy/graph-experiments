import amr
import penman
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

def amr_to_rdf(amr_string):
  penman_graph = penman.decode(amr_string)
      
  g = Graph()
      
  AMR = Namespace("http://example.org/amr/")
  g.bind("amr", AMR)

  resources = {}

  def get_resource(variable):
    if variable not in resources:
      resources[variable] = URIRef(f"http://example.org/amr/{variable}")
    return resources[variable]

  for triple in penman_graph.triples:
    subject_var, role, object_var = triple

    subject_uri = get_resource(subject_var)

    if role == ':instance':
      g.add((subject_uri, RDF.type, AMR[object_var]))
      g.add((subject_uri, RDFS.label, Literal(object_var)))
    else:
      predicate = AMR[role.lstrip(':')]

      if isinstance(object_var, str) and object_var in penman_graph.variables():
        object_uri = get_resource(object_var)
        g.add((subject_uri, predicate, object_uri))
      else:
        g.add((subject_uri, predicate, Literal(object_var)))
        
  return g.serialize(format="turtle")