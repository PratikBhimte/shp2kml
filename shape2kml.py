import simplekml
import geopandas as gpd
import pandas as pd
import numpy as np
from pyproj import Proj, transform,Transformer
import shapely.ops as sp_ops
from shapely.geometry import Point,MultiPoint,LineString,Polygon,MultiPolygon


def shp2kml(gdf):
  kml = simplekml.Kml()

  shpcols = [x for x in gdf.columns if x!='geometry']
  schema = kml.newschema(name='state_schema')
  [schema.newsimplefield(name=f,type='string') for f in shpcols]

  for i,r in gdf.iterrows():
      dnames = [str(x) for x in r.index if x!='geometry']
      dvalues = [str(y) for x,y in zip(r.index,r) if x!='geometry']
      #print(dvalues)
      px = kml.newmultigeometry(name="|".join(dvalues))
      px.extendeddata.schemadata.schemaurl = schema.name

      [px.extendeddata.schemadata.newsimpledata(n,v) for n,v in zip(dnames,dvalues)]

      if r['geometry'].type=='MultiPolygon':
          for poly in (r['geometry']):
              
              npx = px.newpolygon()
              npx.outerboundaryis = (list(poly.exterior.coords))


      elif r['geometry'].type == 'Polygon':
          npx = px.newpolygon()
          npx.outerboundaryis = (list(r['geometry'].exterior.coords))

      elif r['geometry'].type == 'LineString':
          
          npx =px.newlinestring()
          npx.coords = (list(r['geometry'].coords))
          
      elif r['geometry'].type == 'Point':
          npx = px.newpoint()
          npx.coords = (list(r['geometry'].coords))

