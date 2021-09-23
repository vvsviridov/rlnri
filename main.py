

def p_n_offset(attr, value):
    p_n_list = ['kOffset', 'lOffset', 'offset', 'tROffset']
    if attr in p_n_list:
        return attr + ('N' if value < 0 else 'P')
    return attr


def rlnrc_fmt(attrs, fmt):
    return ','.join([f'{p_n_offset(k, v)}={v}' for k, v in attrs.items() if k in fmt])


def rlgnc_fmt(attrs):
    fmt = ['gprsValid', 'pROffset']
    return ','.join([f'{k}={v}' for k, v in attrs.items() if k in fmt])


def relation_json_to_mml(relation_json):
    result = []
    fmt_list = [
        ['cs', 'cand', 'awOffset', 'offset',
         'bqOffsetAfr', 'bqOffsetAwb',
         'bqOffset', 'hiHyst', 'loHyst'],
        ['relType'],
        ['lOffset', 'tRHyst', 'kOffset',
         'lHyst', 'tROffset', 'kHyst'],
    ]
    cell = relation_json['sourceFdn'].split('=')[-1]
    cellr = relation_json['targetFdn'].split('=')[-1]
    result.append(f'RLNRI:CELL={cell},CELLR={cellr};')
    rel_attrs = relation_json['attributes']['GeranCellRelation']
    rel_attrs.pop('relationDirection')
    result.append(f'RLGNC:CELL={cell},CELLR={cellr},{rlgnc_fmt(rel_attrs)};')
    for fmt in fmt_list:
        result.append(
            f'RLNRC:CELL={cell},CELLR={cellr},{rlnrc_fmt(rel_attrs, fmt)};')
    return result


def main(geran_cell_relations):
    for rel in geran_cell_relations:
        print('\n'.join(relation_json_to_mml(rel)).upper())


if __name__ == '__main__':
    geran_cell_relations = [
        {
            "responseLevel": "high",
            "name": "createRelation",
            "sourceFdn": "MeContext=BSC,ManagedElement=BSC,BscFunction=1,BscM=1,GeranCellM=1,GeranCell=Cell1",
            "relationType": "GeranCellRelation",
            "targetFdn": "MeContext=BSC,ManagedElement=BSC,BscFunction=1,BscM=1,GeranCellM=1,GeranCell=Cell2",
            "attributes": {
                "GeranCellRelation": {
                    "bqOffsetAfr": 0,
                    "bqOffsetAwb": 0,
                    "lOffset": 0,
                    "offset": 0,
                    "tRHyst": 0,
                    "kOffset": 0,
                    "lHyst": 0,
                    "relType": "NEUTRAL",
                    "gprsValid": "YES",
                    "bqOffset": 0,
                    "hiHyst": 0,
                    "tROffset": 0,
                    "cand": "BOTH",
                    "awOffset": 0,
                    "kHyst": 0,
                    "loHyst": 0,
                    "relationDirection": "MUTUAL"
                }
            }
        }
    ]
    main(geran_cell_relations)
