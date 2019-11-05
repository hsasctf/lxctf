from sqlalchemy import MetaData
from sqlalchemy.dialects.mysql import pymysql
from sqlalchemy.orm import class_mapper
from sqlalchemy_schemadisplay import create_schema_graph, create_uml_graph

from db import models as model
from db.database import Base


# lets find all the mappers in our model
mappers = []
for attr in dir(model):
    if attr[0] == '_': continue
    try:
        cls = getattr(model, attr)
        mappers.append(class_mapper(cls))
    except:
        pass

# pass them to the function and set some formatting options
graph = create_uml_graph(mappers,
    show_operations=False, # not necessary in this case
    show_multiplicity_one=False # some people like to see the ones, some don't
)
graph.write_pdf('uml.pdf') # write out the file


graph = create_schema_graph(metadata=MetaData('mysql://root:bang2gah7mae0wiegaekooleihe2yeecie8aNee2@localhost/ctf2'),
                            show_datatypes=False,  # The image would get nasty big if we'd show the datatypes
                            show_indexes=False,  # ditto for indexes
                            #rankdir='LR',  # From left to right (instead of top to bottom)
                            concentrate=False  # Don't try to join the relation lines together
)
graph.write_pdf('schema.pdf') # write out the file

