(import click)

(import [slot.store [Store]])

(with-decorator
  (.command click)
  (.argument click "store_name")
  (defn options [store-name]
    (setv store (Store store-name))

    (for
      [option store.options]
      (do
        (setv is-selected (= store.selected-option option))
        (setv prelude (if is-selected "->" "  ")))

        (.secho click
                (.format "{} {}" prelude option)
                :fg (if is-selected "cyan" None)
                :bold is-selected))))
