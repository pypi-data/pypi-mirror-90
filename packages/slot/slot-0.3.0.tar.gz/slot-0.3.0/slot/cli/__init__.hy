(import click)

(import [.stores [stores]])
(import [.list [list-stores]])
(import [.use [use]])
(import [.options [options]])

(with-decorator
  (.group click)
  (defn cli [] None))

(for
  [cmd [stores use options]]
  (.add-command cli cmd))

(.add-command cli list-stores :name "list")
