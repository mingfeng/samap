from django.conf import settings
from django.db import connections
from django.contrib.gis.geos import GEOSGeometry


def get_service_area(location, distance):
    vertex_id = get_nearest_vertex_id(location)
    return get_service_area_from_vertex(vertex_id, distance)


def get_service_area_from_vertex(vertex_id, distance):
    sql = '''
    SELECT pgr_pointsAsPolygon ($$
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
                                %s, %s)) AS dd ON v.id = dd.node $$);
    '''
    with connections['routing'].cursor() as cursor:
        cursor.execute(sql, [vertex_id, distance])
        row = cursor.fetchone()
    return GEOSGeometry(row[0], srid=settings.SRID)


def get_nearest_vertex_id(location):
    sql = "SELECT id FROM roads_vertices_pgr ORDER BY the_geom <-> '{0}'::geometry limit 1".format(location)
    with connections['routing'].cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
    return row[0]
