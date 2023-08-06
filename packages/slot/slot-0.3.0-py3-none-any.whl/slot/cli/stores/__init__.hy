(import click)

(import [.create [create]])
(import [.ingest [ingest]])

(with-decorator (.group click)
  (defn stores [] None))

(for
  [cmd [create ingest]]
  (.add-command stores cmd))
