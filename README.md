[[Tasks]]
# Root files : a

| Makefile       | automatise les commandes du projet (install, run, debug, lint, clean...)                    |
| -------------- | ------------------------------------------------------------------------------------------- |
| Pyproject.toml | liste des dépendances + métadonée du projet (nom, version, python requis)                   |
| uv.lock        | versions exactes figées de toutes les dépendances -> a commit                               |
| .venv/         | environnement virtuel Python réel (l'installation physique des packages) -> a jamais commit |
| .flake8        | config du flake8                                                                            |
| .gitignore     | liste des fichiers/dossiers à exlure de git                                                 |

| main.py   | parse les args puis lance la simulation                                                    |
| --------- | ------------------------------------------------------------------------------------------ |
| flyin/    | mes classes (Zone, Drone, Connection, Parses, Simulation, pathfinding, visualiseur pygame) |
| maps/     | fichiers maps                                                                              |
| tests/    | tests pytest (verif edge cases)                                                            |
| README.md | descriptions, instructions, ressources, choix d'algo, docs                                 |

---

# Zone.py

A ***zone*** is a node of the network, a waypoint for the ***drones***. The Network will be a bunch of ***zones*** linked by ***connections***.
##### Python Concepts
-  **Enum** is a special class used to create a set of named constants to make de code more readable and safer by preventing errors from using invalid values. It make coding easier cause :
	- autocompletion in vscode
	- crashes right away (red underlines)
	Used it for creating ***zones type***

- **Match / Case** works like if/elif but easier. We can raised errors inside a case. Used it for assigning the ***moves costs*** of the drones for each zone types.

- **Pydantic** makes python data reliable. Errors a caught early and failures are explicit. Pydantic converts strings input in the type asked with less code and less manual parsing.
-  ```python
Field(default_factory=set) # Tells pydantic to create another fresh set for each zones.
	```


##### Methods Walkthrough

1. **has_capacity()**
	- returns True if ***start*** or ***end zones***.
	-  otherwise, compares hmany ***drones*** currently occupied the zone against ***max_drones***.
2. add_drone() / remove_drone()
	- check is capacity == full of if it is already in the set
	- add/remove ***drone_id*** to zone.***current_occupants*** (set of drone_id's)

---
# Connections.py

A ***connection*** is an edge of the network, what drones actually travel through to get from one zone to another.

##### Methods Walkthrough
- other_side(), given one endpoint, returns the other one
- has_capacity(), same as the zone one but without the "start/end" check.

---
# Drone.py

A ***drone*** is a moving agent, not part of the static network. it's created and updated by the ***simulation***, not the ***parser***.

##### Methods Walkthrough
None, ***Drone.py*** has only data in it.

---
# Network.py

***Network*** ties everything together. Every zone, every connection.

##### Python Concepts
- Plain class, not a pydantic BaseModel. Cause **Zone**, **Connection** and **Drone** validate a fixed shape of data handed to them all at one. **Network** isn't like that: it start empty then gets built incrementally, one ***add_zone*** / ***add_connection*** call at a time, by the parser.
- ***dict.setdefault(key, default)*** returns ***d[key]*** if it exist, otherwise sets ***d[key] = default*** 
- Nested **list** inside **dict**: ***dict[str, list[Connection]]*** .

##### Concepts
- **adjacency**: *dict[str, list[Connection]]*
	- The actual graph structure: zone name -> connections reachable from it. This is what neighbors() / pathfinding will actually walk, zones and connections alone aren't enough on their own.

##### Methods Walkthrough
- add_zone(): raise ValueError if duplicate name, otherwise register it in zones.
- add_connection(): three checks before anything gets added.
	- Both zone_a / zone_b must already exist in zones
	- The connection can't be a duplicate of one that already exists
	- If good, the connection gets added in connections[], then get registered in adjacency{} both ways.
- neighbors(zone_name): adjacency.get(zone_name, []) so it returns an empty list if a zone has no connections, not a crash with KeyError.

