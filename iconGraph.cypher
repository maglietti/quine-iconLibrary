MATCH (a), (b), (c)
WHERE (a) = idFrom({group[0]})
  AND (b) = idFrom({group[1]})
  AND (c) = idFrom({icon_name["value"]})
SET a:{group[0]}, a.name = {group[0]}
SET b:{group[1]}, b.name = {group[1]}
SET c:{icon_name["value"].replace("-", "_")}, c.name = icon_name["value"]
CREATE (a)<-(b)<-(c)

MATCH (a), (c)
WHERE (a) = idFrom({group[0]})
  AND (c) = idFrom({icon_name["value"]})
SET a:{group[0]}, a.name = {group[0]}
SET c:{icon_name["value"].replace("-", "_")}, c.name = icon_name["value"]
CREATE (a)<-(c)