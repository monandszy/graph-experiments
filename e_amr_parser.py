import amrlib

def parse_english(input: list[str]) -> list[str]:
  stog = amrlib.load_stog_model()
  graphs = stog.parse_sents(input)
  # for graph in graphs:
  #     print(graph)
  return graphs

def parse_amr(graphs: list[str]) -> list[str]:
  gtos = amrlib.load_gtos_model()
  if not graphs:
    return []
  sents = gtos.generate(graphs, disable_progress=True)
  return sents
