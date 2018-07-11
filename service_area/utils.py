from django.db import connections
from django.conf import settings
from django.contrib.gis.geos import Point


def get_service_area(x, y, distance):
    vertex_id = get_nearest_vertex_id(x, y)
    return get_service_area_from_vertex(vertex_id, distance)


def get_service_area_from_vertex(vertex_id, distance):
    sql = '''
    SELECT
    ST_AsGeoJSON (pgr_pointsAsPolygon ($$
            SELECT
                id::integer,
                ST_X (the_geom)::float AS x,
                ST_Y (the_geom)::float AS y
            FROM
                roads_vertices_pgr v
            INNER JOIN (
                    SELECT
                        node
                    FROM
                        pgr_drivingDistance (''
                            SELECT
                                gid AS id,
                                source,
                                target,
                                length AS COST,
                                length AS reverse_cost
                            FROM
                                roads '',
                                %s, %s)) AS dd ON v.id = dd.node $$));
    '''
    with connections['routing'].cursor() as cursor:
        cursor.execute(sql, [vertex_id, distance])
        row = cursor.fetchone()
    return row[0]


def get_nearest_vertex_id(x, y):
    point = Point(x, y, srid=settings.SRID)
    sql = "SELECT id FROM roads_vertices_pgr ORDER BY the_geom <-> '{0}'::geometry limit 1".format(point)
    with connections['routing'].cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
    return row[0]
